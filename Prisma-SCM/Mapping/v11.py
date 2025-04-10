import pandas as pd
import re

# File paths
objects_file = r"C:\Users\DELL\Desktop\output\export_objects_addresses1.csv"
rulebase_file = r"C:\Users\DELL\Desktop\output\export_policies_security_rulebase3.csv"
output_file = r"C:\Users\DELL\Desktop\output\updated_export_objects_addresses11.csv"

# Read CSV files
objects_df = pd.read_csv(objects_file)
rulebase_df = pd.read_csv(rulebase_file)

# Ensure column names are correctly referenced and stripped of whitespace
objects_df.columns = objects_df.columns.str.strip()
rulebase_df.columns = rulebase_df.columns.str.strip()

# Verify required columns exist
if "Address" not in objects_df.columns or "Source Address" not in rulebase_df.columns:
    raise KeyError("Required columns not found in the CSV files. Check column names.")

# Extract known addresses from objects file
known_addresses = set(objects_df["Address"].dropna().astype(str))

# Extract and split unique addresses from rulebase that are missing in objects
rulebase_addresses = set()
for addresses in rulebase_df["Source Address"].dropna().astype(str):
    rulebase_addresses.update(addresses.split(";"))

missing_addresses = rulebase_addresses - known_addresses

# Function to determine the type based on address pattern
def determine_type(address):
    if "-" in address:
        return "IPrange"
    elif "/" in address:
        return "Ip Netmask"
    elif re.search(r"\.(com|org|net|edu|gov)$", address):
        return "Fqdn"
    else:
        return "Unknown"

# Prepare new entries for missing addresses
custom_entries = []

def generate_custom_name(index):
    return f"Custom-Address-{index+1}"

for index, address in enumerate(sorted(missing_addresses)):
    custom_entries.append({
        "Name": generate_custom_name(index),
        "Location": "",  # Keep as blank if not needed
        "Type": determine_type(address),
        "Address": address,
        "Split Addresses": address  # New column for separated values
    })

# Append new entries to the existing dataframe
updated_df = pd.concat([objects_df, pd.DataFrame(custom_entries)], ignore_index=True)

# Save the updated dataframe to a new CSV file
updated_df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Updated object addresses saved to {output_file}")
