import torch
import torch.nn as nn
import numpy as np
from torch.nn import functional as F
import cv2
import os

class ResidualDenseBlock(nn.Module):
    """Residual Dense Block"""
    def __init__(self, nf=64, gc=32, bias=True):
        super(ResidualDenseBlock, self).__init__()
        self.conv1 = nn.Conv2d(nf, gc, 3, 1, 1, bias=bias)
        self.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1, bias=bias)
        self.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1, bias=bias)
        self.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1, bias=bias)
        self.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1, bias=bias)
        self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
        return x5 * 0.2 + x

class RRDB(nn.Module):
    """Residual in Residual Dense Block"""
    def __init__(self, nf, gc=32):
        super(RRDB, self).__init__()
        self.rdb1 = ResidualDenseBlock(nf, gc)
        self.rdb2 = ResidualDenseBlock(nf, gc)
        self.rdb3 = ResidualDenseBlock(nf, gc)

    def forward(self, x):
        out = self.rdb1(x)
        out = self.rdb2(out)
        out = self.rdb3(out)
        return out * 0.2 + x

class RRDBNet(nn.Module):
    """RRDB-based Generator"""
    def __init__(self, in_nc=3, out_nc=3, nf=64, nb=23, gc=32):
        super(RRDBNet, self).__init__()
        self.conv_first = nn.Conv2d(in_nc, nf, 3, 1, 1, bias=True)
        self.body = nn.ModuleList()
        for _ in range(nb):
            self.body.append(RRDB(nf, gc))
        self.conv_body = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        
        # Upsampling layers
        self.upconv1 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.upconv2 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.conv_hr = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.conv_last = nn.Conv2d(nf, out_nc, 3, 1, 1, bias=True)
        self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

    def forward(self, x):
        feat = self.conv_first(x)
        body_feat = feat
        for block in self.body:
            body_feat = block(body_feat)
        trunk = self.conv_body(body_feat)
        feat = trunk + feat
        
        # Upsampling
        feat = F.interpolate(feat, scale_factor=2, mode='nearest')
        feat = self.lrelu(self.upconv1(feat))
        feat = F.interpolate(feat, scale_factor=2, mode='nearest')
        feat = self.lrelu(self.upconv2(feat))
        
        out = self.lrelu(self.conv_hr(feat))
        out = self.conv_last(out)
        return out

class ESRGANUpscaler:
    def __init__(self, model_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Initialize model
        self.model = RRDBNet(
            in_nc=3,
            out_nc=3,
            nf=64,
            nb=23,
            gc=32
        )
        
        # Load model weights with CPU mapping
        try:
            # Try to load with strict=False to ignore missing or unexpected keys
            loadnet = torch.load(model_path, map_location=self.device)
            if 'params_ema' in loadnet:
                self.model.load_state_dict(loadnet['params_ema'], strict=False)
            elif 'params' in loadnet:
                self.model.load_state_dict(loadnet['params'], strict=False)
            else:
                self.model.load_state_dict(loadnet, strict=False)
        except Exception as e:
            print(f"Warning: Error loading model weights: {str(e)}")
            raise
            
        self.model.eval()
        self.model = self.model.to(self.device)
    
    def preprocess_image(self, img):
        """Convert image to tensor and normalize."""
        if len(img.shape) == 2:  # Grayscale
            # Convert to uint8 before color conversion
            img = (img * 255).astype(np.uint8)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            img = img.astype(np.float32)
        
        # Convert to float and normalize to [0, 1]
        img = img.astype(np.float32) / 255.
        
        # HWC to CHW
        img = np.transpose(img, (2, 0, 1))
        
        # To tensor
        img = torch.from_numpy(img).float()
        return img.unsqueeze(0)  # Add batch dimension
    
    def postprocess_image(self, tensor):
        """Convert tensor back to numpy image."""
        tensor = tensor.squeeze(0)  # Remove batch dimension
        img = tensor.float().cpu().clamp_(0, 1).numpy()
        img = np.transpose(img, (1, 2, 0))  # CHW to HWC
        img = (img * 255.0).round().astype(np.uint8)
        return img
    
    def process_tile(self, img_tensor, tile_size=1024, padding=32):
        """Process a single tile of the image."""
        b, c, h, w = img_tensor.size()
        
        # Add padding
        padded = F.pad(img_tensor, (padding,)*4, mode='reflect')
        
        # Forward pass
        with torch.no_grad():
            output = self.model(padded.to(self.device))
        
        # Remove padding
        padding *= 4  # Scale factor is 4
        return output[:, :, padding:-padding, padding:-padding]
    
    def upscale(self, img, tile_size=1024, tile_padding=32):
        """Upscale image with tiled processing."""
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA is not available. This model requires a GPU to run.")
        
        # Preprocess
        img_tensor = self.preprocess_image(img)
        b, c, h, w = img_tensor.size()
        
        # Initialize output tensor
        output = torch.zeros((b, c, h*4, w*4))
        
        # Process tiles
        for i in range(0, h, tile_size):
            for j in range(0, w, tile_size):
                # Extract tile
                tile = img_tensor[:, :, 
                                i:min(i + tile_size, h),
                                j:min(j + tile_size, w)]
                
                # Process tile
                upscaled_tile = self.process_tile(tile, 
                                                tile_size=tile_size,
                                                padding=tile_padding)
                
                # Place tile in output
                output[:, :,
                      i*4:min(i + tile_size, h)*4,
                      j*4:min(j + tile_size, w)*4] = upscaled_tile
        
        # Postprocess
        return self.postprocess_image(output)
