import requests
import pandas as pd
from getpass import getpass

# Firewall API details
fw_ip = "192.168.0.104"
api_url = f"https://{fw_ip}/restapi/v11.1/Policies/SecurityRules?location=vsys&vsys=vsys1"  # Corrected location

# Ask for username & password
username = input("Enter Firewall Username: ")
password = getpass("Enter Firewall Password: ")  # Secure password input

# API Request Headers
headers = {"Content-Type": "application/json"}

# Make API request to fetch security rules
response = requests.get(api_url, auth=(username, password), headers=headers, verify=False)

if response.status_code == 200:
    policies = response.json()  # Extract JSON response
    print("Successfully fetched security policies.")

    # Load the CSV file
    csv_file = r"C:\Users\DELL\Desktop\firewall_policy.csv"
    df = pd.read_csv(csv_file)

    # Ensure "wildfire_analysis" column exists
    if "wildfire_analysis" not in df.columns:
        df["wildfire_analysis"] = ""

    # Iterate through policies and check for missing "wildfire_analysis"
    for index, row in df.iterrows():
        policy_name = row.get("name", "Unknown Policy")  # Get policy name
        wildfire_analysis = row.get("wildfire_analysis", "").strip()

        # If Wildfire Analysis is missing, ask the user to provide a value
        if wildfire_analysis == "":
            new_value = input(f"Enter Wildfire Analysis profile for policy '{policy_name}': ")
            df.at[index, "wildfire_analysis"] = new_value  # Update the value

    # Save the updated CSV
    updated_csv_file = r"C:\Users\DELL\Desktop\firewall_policy.csv"
    df.to_csv(updated_csv_file, index=False)
    
    print(f"Updated CSV saved at: {updated_csv_file}")

else:
    print(f"Failed to fetch security policies. Status Code: {response.status_code}, Error: {response.text}")
