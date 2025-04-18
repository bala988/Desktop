import csv
import http.client
import json

# Define API connection
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiYWM4MDk1MTgtZDMyMS00ZWEyLTgyNjgtODVmZGFhYjA4NjU0LTMxNDg1NTg1Iiwic3VibmFtZSI6IjI3YTY5ZDM0LTdhMTUtNGY1NC04NjRmLWVlYWI3OTY1OGUwNCIsImlzcyI6Imh0dHBzOi8vYXV0aC5hcHBzLnBhbG9hbHRvbmV0d29ya3MuY29tOjQ0My9hbS9vYXV0aDIiLCJ0b2tlbk5hbWUiOiJhY2Nlc3NfdG9rZW4iLCJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiYXV0aEdyYW50SWQiOiJlSlA0N1J3ckdBczdZTjk2RUZMU2pjWEZxQ0UiLCJhdWQiOiJ1c2VyMUAxNjkyMTgzMjA1LmlhbS5wYW5zZXJ2aWNlYWNjb3VudC5jb20iLCJuYmYiOjE3NDE1OTEyOTYsImdyYW50X3R5cGUiOiJjbGllbnRfY3JlZGVudGlhbHMiLCJzY29wZSI6WyJwcm9maWxlIiwidHNnX2lkOjE2OTIxODMyMDUiLCJlbWFpbCJdLCJhdXRoX3RpbWUiOjE3NDE1OTEyOTYsInJlYWxtIjoiLyIsImV4cCI6MTc0MTU5MjE5NiwiaWF0IjoxNzQxNTkxMjk2LCJleHBpcmVzX2luIjo5MDAsImp0aSI6IkpyT0dMaS1zMzRtSVVtV09UQWVDbFhiXzlmdyIsInRzZ19pZCI6IjE2OTIxODMyMDUiLCJhY2Nlc3MiOnsicHJuOjE2OTIxODMyMDU6Ojo6IjpbInN1cGVydXNlciIsImJhc2UiXX19.PFdMJVabVcv-rY_nDVaeLyzH2Dk_BdWKlqm5BbyssBvdWinJLhEIaAXlFi0YGzDpiSGQl5jtWJnrvmnITo9se-nuwcoSOtGBJlMkEsOR-ap5NHPXmVtdow6nLo5T2fioGyKTj6vnvvAFvkSDBY9Z1HBLUQvL49zw-jJEYvr3CFVUm8RLtccsqXs8P7WQxXBwijxkqehWsHtf8-p2fCdYY_-_tHk8KfHQfafnuVUC95fwLFR686huqAGEqocSejX0_ZGMp5Iq34Ow5A2SOhmo82lrCx109PBGvsQTmTz3BEqHvcYxqnsUMC9HJbU3aDUmshhOup3FXBZUdqgl1JHLDA'
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
with open(csv_file, mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        # Extract values
        name = row.get("Name", "").strip()
        description = row.get("Description", "").strip()
        addresses = row.get("Addresses", "").strip()  # Now using "Addresses" instead of "Static"
        tag = row.get("Tags", "").strip()

        # Skip rows with missing essential fields
        if not name or not addresses:
            print(f"Skipping row due to missing name or address group members: {row}")
            continue

        # Convert address objects from semicolon-separated format to list
        address_list = [addr.strip() for addr in addresses.split(";")]

        payload = json.dumps({
            "description": description if description else f"Auto-imported address group {name}",
            "name": name,
            "tag": [tag] if tag else [],
            "static": address_list
        })

        # Send API request to the selected folder
        api_url = f"/sse/config/v1/address-groups?folder={selected_folder.replace(' ', '%20')}"
        conn.request("POST", api_url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(f"Response for {name}: {data.decode('utf-8')}")

# Close the connection
conn.close()
