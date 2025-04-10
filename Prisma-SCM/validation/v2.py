import pandas as pd

def remove_unknown_type_and_duplicates(input_file, output_file):
    # Load the CSV file
    df = pd.read_csv(input_file)
    
    # Ensure column names are correctly referenced and stripped of whitespace
    df.columns = df.columns.str.strip()
    
    # Check if required columns exist
    if "Type" not in df.columns or "Name" not in df.columns or "Address" not in df.columns:
        print("Error: Required columns ('Type', 'Name', 'Address') not found in the CSV file.")
        return
    
    # Remove rows where 'Type' is 'Unknown'
    df = df[df["Type"].astype(str) != "Unknown"]

    # Remove rows where 'Address' matches an existing 'Name'
    df = df[~df["Address"].isin(df["Name"])]

    # Save the filtered dataframe to a new CSV file
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"Filtered file saved as: {output_file}")

# Example usage
input_csv = r"C:\Users\DELL\Desktop\output\updated_export_objects_addresses12.csv"  # Input file path
output_csv = r"C:\Users\DELL\Desktop\output\updated_filtered_output2.csv"  # Output file path
remove_unknown_type_and_duplicates(input_csv, output_csv)

print("Next step: Security rules")
