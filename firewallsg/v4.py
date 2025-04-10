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

# Iterate over each row in the CSV
for _, row in df.iterrows():
    profile_column = row.get("profile", "").strip().lower()
    profile_group = row.get("profile_group", "").strip().lower()

    # If profile group is present or wildfire analysis is already in profile, skip the policy
    if profile_group or "wildfire" in profile_column:
        print(f"Skipping policy '{row.get('name', '')}' due to existing profile group or wildfire analysis.")
        continue
    
    # Case: Wildfire analysis is missing from the profile
    policy_rule = {
        "name": row.get("name", "").strip(),
        "fromzone": row.get("fromzone", "").split(","),
        "tozone": row.get("tozone", "").split(","),
        "source": row.get("source", "").split(","),
        "destination": row.get("destination", "").split(","),
        "action": row.get("action", "allow").strip(),
        "profile": row.get("profile", "") + ",wildfire-analysis",  # Add wildfire analysis
    }
    
    # Prompt user for the wildfire analysis profile if needed
    if "wildfire-analysis" not in profile_column:
        wildfire_analysis = input(f"Enter Wildfire Analysis profile for policy '{policy_rule['name']}': ")
        policy_rule["profile"] = policy_rule["profile"] + "," + wildfire_analysis

    policy_rules.append(policy_rule)

# Construct the payload for API request
payload = {"entry": policy_rules}

# Send the policy updates to the firewall
response = requests.post(api_url, auth=(username, password), headers=headers, json=payload, verify=False)

# Check the response
if response.status_code == 200:
    print("Successfully updated policies to the firewall.")
else:
    print(f"Failed to update policies. Status Code: {response.status_code}, Error: {response.text}")
