import http.client
import json
import csv

# Mapping folder selection to API endpoints
folder_mapping = {
    "1": "Shared",
    "2": "Mobile%20Users",
    "3": "Remote%20Networks",
    "4": "Service%20Connections",
    "5": "Mobile%20Users%20Container",
    "6": "Mobile%20Users%20Explicit%20Proxy"
}

# Prompt user for folder selection
print("Select a folder:")
for key, value in folder_mapping.items():
    print(f"{key}. {value.replace('%20', ' ')}")
folder_choice = input("Enter the number corresponding to the folder: ")

folder = folder_mapping.get(folder_choice)
if not folder:
    print("Invalid selection.")
    exit()

# Define API connection
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiYWM4MDk1MTgtZDMyMS00ZWEyLTgyNjgtODVmZGFhYjA4NjU0LTMxNDg1NTg1Iiwic3VibmFtZSI6IjI3YTY5ZDM0LTdhMTUtNGY1NC04NjRmLWVlYWI3OTY1OGUwNCIsImlzcyI6Imh0dHBzOi8vYXV0aC5hcHBzLnBhbG9hbHRvbmV0d29ya3MuY29tOjQ0My9hbS9vYXV0aDIiLCJ0b2tlbk5hbWUiOiJhY2Nlc3NfdG9rZW4iLCJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiYXV0aEdyYW50SWQiOiJlSlA0N1J3ckdBczdZTjk2RUZMU2pjWEZxQ0UiLCJhdWQiOiJ1c2VyMUAxNjkyMTgzMjA1LmlhbS5wYW5zZXJ2aWNlYWNjb3VudC5jb20iLCJuYmYiOjE3NDE1OTEyOTYsImdyYW50X3R5cGUiOiJjbGllbnRfY3JlZGVudGlhbHMiLCJzY29wZSI6WyJwcm9maWxlIiwidHNnX2lkOjE2OTIxODMyMDUiLCJlbWFpbCJdLCJhdXRoX3RpbWUiOjE3NDE1OTEyOTYsInJlYWxtIjoiLyIsImV4cCI6MTc0MTU5MjE5NiwiaWF0IjoxNzQxNTkxMjk2LCJleHBpcmVzX2luIjo5MDAsImp0aSI6IkpyT0dMaS1zMzRtSVVtV09UQWVDbFhiXzlmdyIsInRzZ19pZCI6IjE2OTIxODMyMDUiLCJhY2Nlc3MiOnsicHJuOjE2OTIxODMyMDU6Ojo6IjpbInN1cGVydXNlciIsImJhc2UiXX19.PFdMJVabVcv-rY_nDVaeLyzH2Dk_BdWKlqm5BbyssBvdWinJLhEIaAXlFi0YGzDpiSGQl5jtWJnrvmnITo9se-nuwcoSOtGBJlMkEsOR-ap5NHPXmVtdow6nLo5T2fioGyKTj6vnvvAFvkSDBY9Z1HBLUQvL49zw-jJEYvr3CFVUm8RLtccsqXs8P7WQxXBwijxkqehWsHtf8-p2fCdYY_-_tHk8KfHQfafnuVUC95fwLFR686huqAGEqocSejX0_ZGMp5Iq34Ow5A2SOhmo82lrCx109PBGvsQTmTz3BEqHvcYxqnsUMC9HJbU3aDUmshhOup3FXBZUdqgl1JHLDA'
}

# CSV file path
csv_file = r"C:\Users\DELL\Desktop\output\export_objects_services1.csv"

# Function to check if a service already exists
def service_exists(service_name, folder):
    conn.request("GET", f"/sse/config/v1/services/{service_name}?folder={folder}", headers=headers)
    res = conn.getresponse()
    data = res.read().decode('utf-8')
    
    response_json = json.loads(data)
    return "_errors" not in response_json  # If no errors, the service exists

# Read and process CSV
with open(csv_file, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        name = row.get("Name", "").strip()
        protocol = row.get("Protocol", "").strip().lower()
        port = row.get("Destination Port", "").strip()
        source_port = row.get("Source Port", "").strip()

        if not name or not protocol or not port:
            print(f"Skipping row due to missing required fields: {row}")
            continue

        # Skip if the service already exists
        if service_exists(name, folder):
            print(f"Skipping {name}: Service already exists.")
            continue

        # Construct protocol-specific payload
        protocol_payload = {
            protocol: {
                "port": port,
                **({"source_port": source_port} if source_port else {})
            }
        }

        # Add override settings only for TCP
        if protocol == "tcp":
            protocol_payload["tcp"]["override"] = {
                "halfclose_timeout": 120,
                "timeout": 3600,
                "timewait_timeout": 15
            }

        payload = json.dumps({
            "description": row.get("Description", ""),
            "name": name,
            "protocol": protocol_payload,
            "tag": row.get("Tags", "").split(";") if row.get("Tags") else []
        })

        # Send API request
        conn.request("POST", f"/sse/config/v1/services?folder={folder}", payload, headers)
        res = conn.getresponse()
        data = res.read()
        
        print(f"Response for {name}: {data.decode('utf-8')}")
