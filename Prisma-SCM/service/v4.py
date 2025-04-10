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
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJyc2Etc2lnbi1wa2NzMS0yMDQ4LXNoYTI1Ni8xIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiYmViODJiZGItNGI4Yi00ODY0LTg0NTUtNGE5NjVkM2Q2NTRhLTE0NTQ4ODc1NCIsInN1Ym5hbWUiOiIyN2E2OWQzNC03YTE1LTRmNTQtODY0Zi1lZWFiNzk2NThlMDQiLCJpc3MiOiJodHRwczovL2F1dGguYXBwcy5wYWxvYWx0b25ldHdvcmtzLmNvbTo0NDMvYW0vb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiOTRjVFV6WFA1RUJHdUJPLXFRbDdJR21vOXBNIiwiYXVkIjoidXNlcjFAMTY5MjE4MzIwNS5pYW0ucGFuc2VydmljZWFjY291bnQuY29tIiwibmJmIjoxNzQwNDc5MDMyLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsicHJvZmlsZSIsInRzZ19pZDoxNjkyMTgzMjA1IiwiZW1haWwiXSwiYXV0aF90aW1lIjoxNzQwNDc5MDMyLCJyZWFsbSI6Ii8iLCJleHAiOjE3NDA0Nzk5MzIsImlhdCI6MTc0MDQ3OTAzMiwiZXhwaXJlc19pbiI6OTAwLCJqdGkiOiJIa0kzYkd3ZWtLZ0JsZDRfRy1lSUtlMUVXLWciLCJ0c2dfaWQiOiIxNjkyMTgzMjA1IiwiYWNjZXNzIjp7InBybjoxNjkyMTgzMjA1Ojo6OiI6WyJzdXBlcnVzZXIiLCJiYXNlIl19fQ.nYzAtBf3XmaLKX1vi9G-38fhkb0YR2BgloOLz77bS_gqe_xTYcXozcQinZoM-xlVPuI0QIQ1-iBUaCXWRYcpKBwxpeqmebiSrlrDtlry6qZ-4QweiCCIF3V1Sa4TV2FPseNzaBnCCI7onn9Co__iFXniHE5CqA5uX8U_3npcZ0758neruIrfb6jPA_CCsKR_hrRrw0g-gGTL3JG9g0fLrL4OCTImyx9_niadyHFyQgjTMH807IIUGeAehMBztG4R-EhLDYyjsA9rPNkfZFvRdP45NVGF-NSW4ppjw-mTaGMuFTvEJHKQxJhaHhFezYB6Ih9ukD6RWKwwxHQ91mNgEw'
}

# CSV file path
csv_file = r"C:\Users\DELL\Desktop\output\export_objects_services1.csv"

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

        # Construct protocol-specific payload
        protocol_payload = {
            protocol: {
                "port": port,
                **({"source_port": source_port} if source_port else {}),  # Include only if not empty
                "override": {
                    "halfclose_timeout": 120,
                    "timeout": 3600,
                    "timewait_timeout": 15
                }
            }
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