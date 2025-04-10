import requests
import csv
import json

# Disable self-signed certificate warnings
requests.packages.urllib3.disable_warnings()

# API Details
api_url = "https://192.168.29.235/restapi/v10.2/Objects/ServiceGroups"
headers = {
    "X-PAN-KEY": "LUFRPT0xR1VhM29hN1NWSTUxSVRuU081d2I5em5OOEE9MkEzM3lDRzVYWkFmSW5Jd0JIdzFuU1pOTXlkR2Y5QVpsUG9scW05RkFSRGFabmFkdW00M2F3SjgvdVg0Zkwycg==",
    "Content-Type": "application/json"
}

# CSV File Path
csv_file = r"C:\Users\DELL\Downloads\objects_service_groups.csv"

# Read CSV and Create Service Groups
with open(csv_file, mode="r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    
    # Clean column names
    reader.fieldnames = [name.strip().replace('"', '') for name in reader.fieldnames]

    print(f"Fixed CSV Columns: {reader.fieldnames}")

    for row in reader:
        try:
            name = row.get("Name", "").strip()
            members = row.get("Services", "").strip()
            
            # Ensure members are in a list format
            if not name or not members:
                print(f"Skipping {name}: Missing name or members")
                continue
            
            service_members = [m.strip() for m in members.split(";") if m.strip()]

            # Modify URL to include the name parameter
            url_with_params = f"{api_url}?location=vsys&vsys=vsys1&name={name}"

            # Construct JSON payload
            body = json.dumps({
                "entry": {
                    "@name": name,
                    "members": {
                        "member": service_members
                    }
                }
            })

            print(f"Sending request to {url_with_params}")
            print(f"Payload for {name}: {body}")

            # Send POST request
            response = requests.post(url_with_params, headers=headers, data=body, verify=False)

            print(f"Response for {name}: {response.status_code} - {response.text}")

            if response.status_code in [200, 201]:
                print(f"Success: {name} added")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Exception occurred for {row}: {str(e)}")
