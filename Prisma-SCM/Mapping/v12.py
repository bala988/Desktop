import pandas as pd
import re

# Load CSV file paths
objects_file = r"C:\Users\DELL\Desktop\output\export_objects_addresses1.csv"
rulebase_file = r"C:\Users\DELL\Desktop\output\export_policies_security_rulebase3.csv"
output_file = r"C:\Users\DELL\Desktop\output\updated_export_objects_addresses12.csv"

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

# Extract unique addresses from rulebase that are missing in objects
rulebase_addresses = set(rulebase_df["Source Address"].dropna().astype(str))
missing_addresses = rulebase_addresses - known_addresses

# Prepare custom grouped entries without removing existing ones
custom_entries = []

def generate_custom_name(index):
    return f"Custom-Address-{index+1}"

def determine_type(address):
    if "-" in address:
        return "IP Range"
    elif "/" in address:
        return "Ip Netmask"
    elif re.search(r"\.(com|org|net|edu|gov)$", address):
        return "FQDN"
    else:
        return "Unknown"

for index, address in enumerate(sorted(missing_addresses)):
    addresses = address.split(";")  # Handle multiple addresses in a single entry
    for addr in addresses:
        if addr not in known_addresses:  # Avoid adding existing addresses
            custom_entries.append({
                "Name": generate_custom_name(index),
                "Location": "",
                "Type": determine_type(addr),
                "Address": addr
            })

# Append new entries to the existing dataframe
updated_df = pd.concat([objects_df, pd.DataFrame(custom_entries)], ignore_index=True)

# Save updated dataframe to CSV
updated_df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Updated object addresses saved to {output_file}")
import pandas as pd
import re

# Load CSV file paths
objects_file = r"C:\Users\DELL\Desktop\output\export_objects_addresses1.csv"
rulebase_file = r"C:\Users\DELL\Desktop\output\export_policies_security_rulebase3.csv"
output_file = r"C:\Users\DELL\Desktop\output\updated_export_objects_addresses12.csv"

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

# Extract unique addresses from rulebase that are missing in objects
rulebase_addresses = set(rulebase_df["Source Address"].dropna().astype(str))
missing_addresses = rulebase_addresses - known_addresses

# Prepare custom grouped entries without removing existing ones
custom_entries = []

def generate_custom_name(index):
    return f"Custom-Address-{index+1}"

def determine_type(address):
    if "-" in address:
        return "IP Range"
    elif "/" in address:
        return "Ip Netmask"
    elif re.search(r"\.(com|org|net|edu|gov)$", address):
        return "FQDN"
    else:
        return "Unknown"

for index, address in enumerate(sorted(missing_addresses)):
    addresses = address.split(";")  # Handle multiple addresses in a single entry
    for addr in addresses:
        if addr not in known_addresses:  # Avoid adding existing addresses
            custom_entries.append({
                "Name": generate_custom_name(index),
                "Location": "",
                "Type": determine_type(addr),
                "Address": addr
            })

# Append new entries to the existing dataframe
updated_df = pd.concat([objects_df, pd.DataFrame(custom_entries)], ignore_index=True)

# Save updated dataframe to CSV
updated_df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Updated object addresses saved to {output_file}")
import pandas as pd
import re

# Load CSV file paths
objects_file = r"C:\Users\DELL\Desktop\output\export_objects_addresses1.csv"
rulebase_file = r"C:\Users\DELL\Desktop\output\export_policies_security_rulebase3.csv"
output_file = r"C:\Users\DELL\Desktop\output\updated_export_objects_addresses12.csv"

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

# Extract unique addresses from rulebase that are missing in objects
rulebase_addresses = set(rulebase_df["Source Address"].dropna().astype(str))
missing_addresses = rulebase_addresses - known_addresses

# Prepare custom grouped entries without removing existing ones
custom_entries = []

def generate_custom_name(index):
    return f"Custom-Address-{index+1}"

def determine_type(address):
    if "-" in address:
        return "IP Range"
    elif "/" in address:
        return "Ip Netmask"
    elif re.search(r"\.(com|org|net|edu|gov)$", address):
        return "FQDN"
    else:
        return "Unknown"

for index, address in enumerate(sorted(missing_addresses)):
    addresses = address.split(";")  # Handle multiple addresses in a single entry
    for addr in addresses:
        if addr not in known_addresses:  # Avoid adding existing addresses
            custom_entries.append({
                "Name": generate_custom_name(index),
                "Location": "",
                "Type": determine_type(addr),
                "Address": addr
            })

# Append new entries to the existing dataframe
updated_df = pd.concat([objects_df, pd.DataFrame(custom_entries)], ignore_index=True)

# Save updated dataframe to CSV
updated_df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Updated object addresses saved to {output_file}")
print("Next step: Validation")

