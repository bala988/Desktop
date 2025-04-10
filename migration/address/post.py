import requests
import csv
import json

# Disable self-signed certificate warnings
requests.packages.urllib3.disable_warnings()

# API Details
api_url = "https://192.168.29.235/restapi/v10.2/Objects/Addresses"
headers = {
    "X-PAN-KEY": "LUFRPT0xR1VhM29hN1NWSTUxSVRuU081d2I5em5OOEE9MkEzM3lDRzVYWkFmSW5Jd0JIdzFuU1pOTXlkR2Y5QVpsUG9scW05RkFSRGFabmFkdW00M2F3SjgvdVg0Zkwycg=="  # Replace with your actual API key
}

# CSV File Path
csv_file = r"C:\Users\DELL\Downloads\address.csv"

# Read CSV and Create Address Objects
with open(csv_file, mode="r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    # Fix CSV column names by removing extra spaces/quotes
    reader.fieldnames = [name.strip().replace('"', '') for name in reader.fieldnames]

    print(f"Fixed CSV Columns: {reader.fieldnames}")  # Debugging column names

    for row in reader:
        try:
            # Strip and clean row values
            name = row.get("Name", "").strip()
            address = row.get("Address", "").strip()
            ip_type = row.get("Type", "").strip().lower()

            if not name or not address or not ip_type:
                print(f"Skipping row due to missing data: {row}")
                continue  # Skip invalid rows

            # Determine the correct key based on type
            if ip_type == "ip netmask":
                ip_key = "ip-netmask"
            elif ip_type == "ip range":
                ip_key = "ip-range"
            elif ip_type == "fqdn":
                ip_key = "fqdn"  # Fix for FQDN not being sent properly
            else:
                print(f"⚠️ Unknown type '{ip_type}', skipping: {row}")
                continue

            # Location parameters
            params = {
                "location": "vsys",  # Updated location type
                "vsys": "vsys1",  # Updated device group name
                "name": name
            }

            # Construct JSON payload
            body = json.dumps({
                "entry": {
                    "@name": name,
                    ip_key: address,  # Now handles FQDN correctly
                }
            })

            print(f"Sending request to {api_url} with params {params}")  # Debugging
            print(f"Payload for {name}: {body}")  # Debugging payload

            # Send POST request
            response = requests.post(api_url, params=params, headers=headers, data=body, verify=False)

            print(f"Response for {name}: {response.status_code} - {response.text}")

            if response.status_code in [200, 201]:
                print(f"✅ Success: {name} added")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"⚠️ Exception occurred for {row}: {str(e)}")
