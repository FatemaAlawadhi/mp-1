import os
import json
import requests
import sys

# Usage: python fetch_project_data.py <TOKEN>
# Or set the environment variable OC_API_TOKEN

def get_token():
    # Default token (replace with your own if needed)
    default_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJEVTFPRFExTURZd09VWXpOMFV6UTBWRE5EZEJRVFJHTUVZMk1FTkdNa0pHUmtZMVJqQkdPQSJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLm9wZW4tY29zbW9zLmNvbS8iLCJzdWIiOiJhdXRoMHw2ODAyMDg4NmQ3YzA0Yjk3NDBiMDczNGEiLCJhdWQiOlsiaHR0cHM6Ly9iZWVhcHAub3Blbi1jb3Ntb3MuY29tIiwiaHR0cHM6Ly9vcGVuY29zbW9zLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3NDUwNDYwNzEsImV4cCI6MTc0NTEzMjQ3MSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtc2Qgb3BzIGRhdGEgaGlsIHBvcnRhbCB1c2VyIHN1YmplY3QgcmVsYXRpb25zaGlwIHJvbGUgbWlzc2lvbiBwcm9ncmFtbWUgb3JnYW5pc2F0aW9uIGVwaGVtZXJpcyBvZmZsaW5lX2FjY2VzcyIsImF6cCI6InR0Zm1qdXV4QTNaWUs0SmtVeTRjRUluNDhrZnFrckV6In0.SfYwqJRgm3nbzURGhwLTcoSQC7lY09C0RMMpu8oYNpZhbm6hrzvodiobt1FYf7Z0x-Q-X-yT1OibG2wqWBI12-txrEju2D2OFWsARU6ZDxI20embWT9QVljG3p27F0wnp9h3fbDRqCzBzB2cTkYN2GNA789txTMSnFREXNKc_mvER-jjFhDnwAU_YYs3P03XmxXqHyGAkVcF6S7XYFIEBSHdDcY3hYHJB1uc4AwmO8uc6BmcYd-zcHKM2t8oPBYNQqIN2M8iCpP7MlGNtHqvS7DtJ137TyCxhqYOXbFajxT8CjiGysj4raMFxDwhxgN1OwX5d5J9sqj0D1U0hZRezg"
    if len(sys.argv) > 1:
        return sys.argv[1]
    token = os.getenv("OC_API_TOKEN")
    if token:
        return token
    if default_token:
        return default_token
    print("Error: No API token provided. Please update the script with your token, pass it as an argument, or set OC_API_TOKEN.")
    sys.exit(1)

def main():
    token = get_token()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    url = "https://app.open-cosmos.com/api/data/v0/scenario/scenario/aa55c71b-f73a-4401-a0be-b7ba662f2c98/search"
    payload = {"query": {}, "limit": 50}
    try:
        response = session.post(url, json=payload)
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
        try:
            response_data = response.json()
            # Save to file
            with open("project_data.json", "w") as f:
                json.dump(response_data, f, indent=4)
            print("API response saved to project_data.json")
            print(json.dumps(response_data, indent=4))
        except json.JSONDecodeError:
            print("Error: Response is not valid JSON. Data not saved.")
            print("Response Text (not JSON):")
            print(response.text)
            sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: Could not connect to {url}. Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: The request timed out while trying to connect to {url}. Error: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} {e.response.reason} for url: {url}. Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
