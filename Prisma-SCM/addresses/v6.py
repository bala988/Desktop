import csv
import http.client
import json

# Define API connection
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiOWU2MzdkODUtNGFmNS00ZDMxLTk1ODEtY2ExYWY4Nzc1YjRiLTE0NDk0NjkzMyIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiV1dBZm5ram85YXM0QllhZUQ0WGhaTFdheXVvIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwNDY4ODMwLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwNDY4ODMwLCJyZWFsbSI6Ii8iLCJleHAiOjE3NDA0Njk3MzAsImlhdCI6MTc0MDQ2ODgzMCwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJMQm5iUWhiNF9GNHdvUER1RFIzUWQ5Mlg5YVEiLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.XaH2t6AOeSbjIqX2pMJmrKcO7G_qh2agoIgDUP5QZsp3oBA0pLZFITPIW62DNdJyG9GYdf6HfVc2wOo48c1fnxM-wTA9IJ7Dye2zSBEDEIagAm4QdrCODmwHAthf_aZeFyn3W9658nvicZKsDmJZwYtVVOEfyhCtQ61eseAWbUzJCv1uvzymihFh8O3EK5iiCWNC7VxYf6y1p37szvudDTb3MygQE7gId2yTSyflOpHPGLLL_fUS2WD7QY1EDEyWDHJydI6Tol-WQasqk3d4Bmro_UWTkREBEbrGKnUy9tqGbBTe4_zveVjp3lleWMb-zy8BIGmaDB28-D_NLnvEnA'
}

# Folder options
folders = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connections",
    "5": "Mobile Users Container",
    "6": "Mobile Users Explicit Proxy"
}

# Display folder options
print("Select a folder to add address objects:")
for key, value in folders.items():
    print(f"{key}. {value}")

# Get user input for folder selection
selected_option = input("Enter the number corresponding to the folder: ").strip()

# Validate user input
if selected_option not in folders:
    print("Invalid selection. Exiting...")
    exit()

selected_folder = folders[selected_option]

# CSV File Path
csv_file = r"C:\Users\DELL\Desktop\output\export_objects_addresses1.csv"

# Read CSV and push data to Prisma Access
with open(csv_file, mode='r', encoding='utf-8-sig') as file:  # Handle BOM
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        # Extract values
        name = row.get("Name", "").strip()
        address_value = row.get("Address", "").strip()
        tag = row.get("Tags", "").strip()
        address_type = row.get("Type", "").strip().lower()  # Convert type to lowercase for consistency

        # Skip rows with missing essential fields
        if not name or not address_value or not address_type:
            print(f"Skipping row due to missing name, address, or type: {row}")
            continue

        # Construct payload dynamically based on address type
        address_payload = {
            "description": f"Auto-imported object {name}",
            "name": name,
            "tag": [tag] if tag else []
        }

        # Assign correct API keys for different types
        if address_type == "ip_netmask":
            address_payload["ip_netmask"] = address_value
        elif address_type == "fqdn":
            address_payload["fqdn"] = address_value
        elif address_type == "ip_wildcard":
            address_payload["ip_wildcard"] = address_value
        elif address_type == "ip_range":
            address_payload["ip_range"] = address_value
        else:
            print(f"Skipping {name} due to invalid address type: {address_type}")
            continue

        # Print payload before sending (for debugging)
        print(f"Sending request for {name}: {json.dumps(address_payload, indent=2)}")

        # Send API request to the selected folder
        payload = json.dumps(address_payload)
        api_url = f"/sse/config/v1/addresses?folder={selected_folder.replace(' ', '%20')}"
        conn.request("POST", api_url, payload, headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')

        # Print API response
        print(f"Response for {name}: {data}")

# Close the connection
conn.close()
