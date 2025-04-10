import pandas as pd

def remove_unknown_type(input_file, output_file):
    # Load the CSV file
    df = pd.read_csv(input_file)
    
    # Ensure column names are correctly referenced and stripped of whitespace
    df.columns = df.columns.str.strip()
    
    # Check if 'Type' column exists
    if "Type" in df.columns:
        # Remove rows where 'Type' is 'Unknown'
        df = df[df["Type"].astype(str) != "Unknown"]
    else:
        print("Error: 'Type' column not found in the CSV file.")
        return
    
    # Save the filtered dataframe to a new CSV file
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"Filtered file saved as: {output_file}")

# Example usage
input_csv = r"C:\Users\DELL\Desktop\output\updated_export_objects_addresses12.csv"  # Change this to the actual input file path
output_csv = r"C:\Users\DELL\Desktop\output\updated_filtered_output.csv"  # Change this to the desired output file path
remove_unknown_type(input_csv, output_csv)

print("Next step: Securityrules")
