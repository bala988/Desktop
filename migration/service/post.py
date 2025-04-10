import requests
import csv
import json

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# API Details
api_url = "https://192.168.29.235/restapi/v10.2/Objects/Services"
headers = {
    "X-PAN-KEY": "LUFRPT0xR1VhM29hN1NWSTUxSVRuU081d2I5em5OOEE9MkEzM3lDRzVYWkFmSW5Jd0JIdzFuU1pOTXlkR2Y5QVpsUG9scW05RkFSRGFabmFkdW00M2F3SjgvdVg0Zkwycg=="  # Replace with actual API key
}

# CSV File Path
csv_file = r"C:\Users\DELL\Downloads\services.csv"

# Read CSV and Create Service Objects
with open(csv_file, mode="r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    # Fix column names by removing extra spaces/quotes
    reader.fieldnames = [name.strip().replace('"', '') for name in reader.fieldnames]
    print(f"Fixed CSV Columns: {reader.fieldnames}")  # Debugging column names

    for row in reader:
        try:
            # Strip and clean row values
            name = row.get("Name", "").strip()
            protocol = row.get("Protocol", "").strip().lower()
            destination_port = row.get("Destination Port", "").strip()

            if not name or not protocol or not destination_port:
                print(f"⚠️ Skipping row due to missing data: {row}")
                continue  # Skip invalid rows

            # Validate protocol
            if protocol not in ["tcp", "udp"]:
                print(f"⚠️ Unknown protocol '{protocol}', skipping: {row}")
                continue

            # Location parameters
            params = {
                "location": "vsys",
                "vsys": "vsys1",
                "name": name
            }

            # Construct JSON payload
            body = json.dumps({
                "entry": {
                    "@name": name,
                    "protocol": {
                        "tcp" if protocol == "tcp" else "udp": {
                            "port": destination_port  # Ensure port is placed inside correct protocol key
                        }
                    }
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
