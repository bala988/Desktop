import csv
import http.client
import json

# Define API connection
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiOWU2MzdkODUtNGFmNS00ZDMxLTk1ODEtY2ExYWY4Nzc1YjRiLTEwMjUxNTQ5OCIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiWEl3Wklsc1c5eXV3TG05RWNncllMSER3RFhzIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzM5NTE2MDYzLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzM5NTE2MDYzLCJyZWFsbSI6Ii8iLCJleHAiOjE3Mzk1MTY5NjMsImlhdCI6MTczOTUxNjA2MywiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJLQXViM1R5bXZZWGlfSEtpRFdGVzQxeW5Jc0UiLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.Ng08-HDCvYXAZflxqDclrapdosaVNuY3k0-rPf-zz5M54Vo_5rEu8RP8ajoMQtBOWPcxaa72OM-teohs4Z0WbPu9I1UL76u_7XSsg9iJhMbxH6VwAO2A7uyYOB0FEKhHiqOrmEhiSMzaZOBc_D0tywuE4pwRNVgoHaQjIsUCmKC_fRZXpWTKgFgum8LNKikOmyX2yo2pIal9NQEVBESoggxox_nnAZiorK2OUhVfGMewe0zlLHx9psJ9XzgK3-ZAS_cIOdW420ZYolQ9M8qRls0WXrZPpu-0Fx2NDn4HAATEY9HyNIUwYZONIPOoKTldmjbzfZlkOxz0DEGnvkNI-A'  # Replace with your actual token
}

# Folder options for Address Groups
folders = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connections",
    "5": "Mobile Users Container",
    "6": "Mobile Users Explicit Proxy"
}

# Display folder options
print("Select a folder to add address groups:")
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
csv_file = r"C:\Users\DELL\Desktop\output\export_objects_address_groups.csv"

# Read CSV and push address groups to Prisma Access
with open(csv_file, mode='r', encoding='utf-8-sig') as file:  # Handle BOM
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        # Extract values
        name = row.get("Name", "").strip()
        description = row.get("Description", "").strip()
        static_objects = row.get("Static", "").strip()  # Comma-separated list of address objects
        tag = row.get("Tags", "").strip()

        # Skip rows with missing essential fields
        if not name or not static_objects:
            print(f"Skipping row due to missing name or address group members: {row}")
            continue

        # Convert static objects from CSV format (comma-separated) to list
        static_objects_list = [obj.strip() for obj in static_objects.split(",")]

        payload = json.dumps({
            "description": description if description else f"Auto-imported address group {name}",
            "name": name,
            "tag": [tag] if tag else [],
            "static": static_objects_list
        })

        # Send API request to the selected folder
        api_url = f"/sse/config/v1/address-groups?folder={selected_folder.replace(' ', '%20')}"
        conn.request("POST", api_url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(f"Response for {name}: {data.decode('utf-8')}")

# Close the connection
conn.close()
