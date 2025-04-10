import csv
import http.client
import json

# Define API connection
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiYmViODJiZGItNGI4Yi00ODY0LTg0NTUtNGE5NjVkM2Q2NTRhLTE1MDg4NzA4MSIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiSlpMM200QUtmcHlROWRWendoS2V5Q1N5Z0FjIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwNTc1NDI3LCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwNTc1NDI3LCJyZWFsbSI6Ii8iLCJleHAiOjE3NDA1NzYzMjcsImlhdCI6MTc0MDU3NTQyNywiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJldmdEYUhwcloyUHIwMzhvNi1DdHA5ZVJyQ28iLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.NqtzCvrNA7MwivD2_zL0Rj0SIcIiaB7fqhZzI1eRNBqPQYotl24fGStO80wI1pfBHV9bLPaZ5mXNW6JV6uSswIYbP5WbpbDm-bZ-r-zl8e5ciX4VUFqhToyOIN7-mOu1HfDzNoXgOUNaBG0Vp0eRu0HaXl-dzwbxf3Ldw9ZgAhTOPhoneJ0cV6bSQqIpzAtfwx7CTJq-XjrGK050qcilslsv_TOw5r-QWUxw8b6IXcEDl3IAQyVCC1QAirc-5qTaoI9688IFwQh0oysZsFQjS97_5UhaKQ__l1YX0xyX8w4LkihQrinL90PkSBR41Phuzi6nhY5sPJFRthpa8B4hJQ'  # Replace with your actual token
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
with open(csv_file, mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        # Extract values
        name = row.get("Name", "").strip()
        address_type = row.get("Type", "").strip().lower()
        address = row.get("Address", "").strip()
        tag = row.get("Tags", "").strip()
        
        # Skip rows with missing essential fields
        if not name or not address_type or not address:
            print(f"Skipping row due to missing required fields: {row}")
            continue
        
        # Map address type correctly
        payload = {
            "description": f"Auto-imported object {name}",
            "name": name,
            "tag": [tag] if tag else []
        }
        
        if address_type == "ip netmask":
            payload["ip_netmask"] = address
        elif address_type == "fqdn":
            payload["fqdn"] = address
        elif address_type == "ip range":
            payload["ip_range"] = address
        elif address_type == "ip wildcard":
            payload["ip_wildcard"] = address
        else:
            print(f"Skipping {name} due to unsupported address type: {address_type}")
            continue
        
        # Convert payload to JSON and send API request
        payload_json = json.dumps(payload, indent=2)
        print(f"Sending request for {name}: {payload_json}")
        
        api_url = f"/sse/config/v1/addresses?folder={selected_folder.replace(' ', '%20')}"
        conn.request("POST", api_url, payload_json, headers)
        res = conn.getresponse()
        data = res.read()
        print(f"Response for {name}: {data.decode('utf-8')}")

# Close the connection
conn.close()