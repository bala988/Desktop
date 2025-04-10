import requests
import csv
import json

# Disable self-signed certificate warnings
requests.packages.urllib3.disable_warnings()

# API Details
api_url = "https://192.168.29.235/restapi/v10.2/Objects/AddressGroups"
headers = {
    "X-PAN-KEY": "LUFRPT0xR1VhM29hN1NWSTUxSVRuU081d2I5em5OOEE9MkEzM3lDRzVYWkFmSW5Jd0JIdzFuU1pOTXlkR2Y5QVpsUG9scW05RkFSRGFabmFkdW00M2F3SjgvdVg0Zkwycg=="
}

# CSV File Path
csv_file = r"C:\Users\DELL\Downloads\objects_address_groups.csv"

# Read CSV and Create Address Groups
with open(csv_file, mode="r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    # Fix CSV column names by removing extra spaces/quotes
    reader.fieldnames = [name.strip().replace('"', '') for name in reader.fieldnames]

    print(f"Fixed CSV Columns: {reader.fieldnames}")  # Debugging column names

    for row in reader:
        try:
            # Extract and clean data
            name = row.get("Name", "").strip()
            addresses = row.get("Addresses", "").strip()

            if not name or not addresses:
                print(f"Skipping {name}: Missing name or addresses")
                continue

            # Convert semicolon-separated addresses into a list
            address_members = [addr.strip() for addr in addresses.split(";") if addr.strip()]

            # API Query Parameters (Required for PAN-OS)
            params = {
                "location": "vsys",  # Required location
                "vsys": "vsys1",      # Specify the vsys (change if needed)
                "name": name          # <== FIX: Added name in query params
            }

            # Construct JSON payload
            body = json.dumps({
                "entry": {
                    "@name": name,
                    "static": {
                        "member": address_members
                    }
                }
            })

            print(f"Sending request to {api_url} with params {params}")
            print(f"Payload for {name}: {body}")

            # Send POST request
            response = requests.post(api_url, headers=headers, params=params, data=body, verify=False)

            print(f"Response for {name}: {response.status_code} - {response.text}")

            if response.status_code in [200, 201]:
                print(f"Success: {name} added")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Exception occurred for {row}: {str(e)}")
