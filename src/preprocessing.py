import pandas as pd
import json
import argparse

def extract_json_data(json_str):
    """
    Extracts 'amount' and 'fee' from a JSON string.

    Args:
    - json_str (str): A string containing JSON data with 'amount' and 'fee' fields.

    Returns:
    - tuple: A tuple containing the amount and fee (both as strings).
    """
    try:
        # Attempt to parse the JSON string
        data = json.loads(json_str.replace("'", "\""))  # Ensure single quotes are replaced with double quotes
        return data.get("amount", ""), data.get("fee", "")
    except json.JSONDecodeError as e:
        # Log the error if JSON parsing fails (consider adding logging for production code)
        print(f"Error decoding JSON: {e}")
        return "", ""


def process_reconciliation_data(input_file, output_file):
    """
    Processes the transaction reconciliation data, filters out 'Not Found-SysB' cases,
    extracts 'amount' and 'fee' from JSON fields, and saves the cleaned data to a CSV file.

    Args:
    - input_file (str): Path to the raw input CSV file containing reconciliation data.
    - output_file (str): Path where the cleaned CSV file will be saved.

    Returns:
    - None
    """
    # Load the data
    df = pd.read_csv(input_file, dtype=str)

    # Fill missing values with empty string to avoid NaN issues
    df.fillna("", inplace=True)

    # Filter rows where 'recon_status' is 'Not Found'
    df = df[df["recon_status"] == "Not Found"]

    # Extract 'amount' and 'fee' from the JSON string in the 'recon_sub_status' column
    df[["sys_b_amount", "sys_b_fee"]] = df["recon_sub_status"].apply(lambda x: pd.Series(extract_json_data(x)))

    # Select relevant columns to keep
    cleaned_df = df[["txn_ref_id", "sys_a_date", "sys_a_amount_attribute_1", "sys_a_amount_attribute_2", "sys_b_amount", "sys_b_fee", "currency_type"]]

    # Save the cleaned dataframe to CSV
    cleaned_df.to_csv(output_file, index=False)
    print(f"Processed file saved as: {output_file}")


def main():
    """
    Main function to parse arguments and process the reconciliation data.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process transaction reconciliation data.")
    parser.add_argument('--input', required=True, help="Path to the raw input CSV file (e.g. data/recon_data_raw.csv).")
    parser.add_argument('--output', required=True, help="Path to save the cleaned CSV file (e.g. data/recon_data_processed.csv).")

    args = parser.parse_args()

    # Process the reconciliation data using the provided input and output paths
    process_reconciliation_data(args.input, args.output)


# Run the script if it is being executed directly
if __name__ == "__main__":
    main()
