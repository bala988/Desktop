import requests
import pandas as pd
import json
from getpass import getpass

# Firewall API details
fw_ip = "192.168.0.104"
api_url = f"https://{fw_ip}/restapi/v11.1/Policies/PolicyBasedForwardingRules?location=vsys&vsys=vsys1"

# Get firewall credentials
username = input("Enter Firewall Username: ")
password = getpass("Enter Firewall Password: ")  # Secure password input

# API Request Headers
headers = {"Content-Type": "application/json"}

# Load the CSV file
csv_file = r"C:\Users\DELL\Desktop\firewall_policy.csv"
df = pd.read_csv(csv_file)

# Convert CSV data to API-compatible JSON format
policy_rules = []
for _, row in df.iterrows():
    policy_rule = {
        "name": row.get("name", "").strip(),
        "fromzone": row.get("fromzone", "").split(","),
        "tozone": row.get("tozone", "").split(","),
        "source": row.get("source", "").split(","),
        "destination": row.get("destination", "").split(","),
        "action": row.get("action", "allow").strip(),
    }

    # Check if 'wildfire_analysis' exists under the 'profile' column
    profile_column = row.get("profile", "").strip()
    if "wildfire" not in profile_column.lower():
        # If wildfire is missing, ask user to provide a value
        wildfire_analysis = input(f"Enter Wildfire Analysis profile for policy '{policy_rule['name']}': ")
        policy_rule["wildfire_analysis"] = wildfire_analysis
    else:
        # If wildfire analysis is already part of the profile, add it to the rule
        policy_rule["wildfire_analysis"] = "wildfire-profile"  # Or use the profile value if you want

    policy_rules.append(policy_rule)

# Construct API payload
payload = {"entry": policy_rules}

# Push rules to the firewall
response = requests.post(api_url, auth=(username, password), headers=headers, json=payload, verify=False)

# Check the response
if response.status_code == 200:
    print("Successfully pushed policies to the firewall.")
else:
    print(f"Failed to push policies. Status Code: {response.status_code}, Error: {response.text}")
