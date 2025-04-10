import requests
import csv
import json

# Disable self-signed certificate warnings
requests.packages.urllib3.disable_warnings()

# API Details
api_url = "https://192.168.29.235/restapi/v10.2/Policies/SecurityRules"
headers = {
    "X-PAN-KEY": "LUFRPT0xR1VhM29hN1NWSTUxSVRuU081d2I5em5OOEE9MkEzM3lDRzVYWkFmSW5Jd0JIdzFuU1pOTXlkR2Y5QVpsUG9scW05RkFSRGFabmFkdW00M2F3SjgvdVg0Zkwycg==",
    "Content-Type": "application/json"
}

# CSV File Path
csv_file = r"C:\Users\DELL\Downloads\policy.csv"

# Read CSV and Create Security Policies
with open(csv_file, mode="r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    # Fix CSV column names by removing extra spaces/quotes
    reader.fieldnames = [name.strip().replace('"', '') for name in reader.fieldnames]

    print(f"Fixed CSV Columns: {reader.fieldnames}")  # Debugging column names

    for row in reader:
        try:
            # Strip and clean row values
            name = row.get("Name", "").strip()
            from_zone = row.get("Source Zone", "").strip()
            to_zone = row.get("Destination Zone", "").strip()
            source_address = row.get("Source Address", "").strip()
            destination_address = row.get("Destination Address", "").strip()
            service = row.get("Service", "").strip()
            application = row.get("Application", "").strip()  # Fetch application
            action = row.get("Action", "").strip().lower()  # Convert action to lowercase

            # Ensure valid action
            valid_actions = ["allow", "deny", "drop", "reset-client", "reset-server", "reset-both"]
            if action not in valid_actions:
                print(f"Invalid action '{action}', defaulting to 'allow'")
                action = "allow"

            if not name or not from_zone or not to_zone or not action:
                print(f"Skipping row due to missing data: {row}")
                continue  # Skip invalid rows

            # Format multiple values properly
            source_members = source_address.split(";") if source_address else ["any"]
            destination_members = destination_address.split(";") if destination_address else ["any"]
            service_members = service.split(";") if service else ["application-default"]
            application_members = application.split(";") if application else ["any"]  # Default to "any"

            # Location parameters
            params = {
                "location": "vsys",
                "vsys": "vsys1",
                "name": name
            }

            # Construct JSON payload
            body = {
                "entry": {
                    "@name": name,
                    "from": {"member": [from_zone]},
                    "to": {"member": [to_zone]},
                    "source": {"member": source_members},
                    "destination": {"member": destination_members},
                    "application": {"member": application_members},  # Added application
                    "service": {"member": service_members},
                    "action": action
                }
            }

            print(f"Sending request to {api_url} with params {params}")  # Debugging
            print(f"Payload for {name}: {json.dumps(body, indent=2)}")  # Debugging payload

            # Send POST request
            response = requests.post(api_url, params=params, headers=headers, json=body, verify=False)

            print(f"Response for {name}: {response.status_code} - {response.text}")

            if response.status_code in [200, 201]:
                print(f"Success: {name} added")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Exception occurred for rule {name}: {str(e)}")
