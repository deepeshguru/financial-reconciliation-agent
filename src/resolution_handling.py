import chardet
import pandas as pd
import ollama
import os
import argparse

# Define output folders
RESOLVED_FOLDER = "resolved_cases"
UNRESOLVED_FOLDER = "unresolved_cases"
PATTERN_DATABASE = "resolution_patterns.csv"

# Create folders if they don't exist
os.makedirs(RESOLVED_FOLDER, exist_ok=True)
os.makedirs(UNRESOLVED_FOLDER, exist_ok=True)

# Load or initialize the pattern database
if os.path.exists(PATTERN_DATABASE):
    try:
        pattern_df = pd.read_csv(PATTERN_DATABASE)
        known_patterns = set(pattern_df["Pattern"].dropna().tolist())
    except pd.errors.EmptyDataError:
        known_patterns = set()
else:
    known_patterns = set()

def query_llm(prompt):
    """
    Queries the Ollama LLM and handles any API errors.
    """
    try:
        response = ollama.chat(
            model="llama3.1:8b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"LLM Query Failed: {e}")
        return "Error: Could not generate response."

def classify_resolution_status(text):
    """
    Classifies the resolution status as 'Resolved' or 'Unresolved'.
    """
    return query_llm(f"Classify the following financial issue as 'Resolved' or 'Unresolved': {text}")

def generate_summary(text):
    """
    Generates a summary for the given financial issue.
    """
    return query_llm(f"Summarize this financial issue: {text}")

def suggest_next_steps(text):
    """
    Suggests next steps for resolving the given financial issue.
    """
    return query_llm(f"Suggest next steps for resolving: {text}")

def identify_resolution_pattern(text):
    """
    Identifies the resolution pattern from the case comments.
    """
    return query_llm(f"Identify resolution pattern from this case: {text}")

def process_resolutions(resolution_file):
    """
    Processes resolution comments from the given file, classifies them as resolved or unresolved,
    and saves the categorized data into respective folders.
    """

    # Detect file encoding
    with open(resolution_file, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']

    # Read CSV with detected encoding
    df = pd.read_csv(resolution_file, encoding=encoding)

    unresolved_data = []
    resolved_data = []
    new_patterns = []

    for _, row in df.iterrows():
        order_id = row["Transaction ID"]
        amount = row["amount"]
        comments = row["Comments"]

        # Step 1: Use LLM to classify as Resolved or Unresolved
        resolution_status = classify_resolution_status(comments)

        if "unresolved" in resolution_status.lower():
            # Step 2: Handle Unresolved Cases
            summary = generate_summary(comments)
            next_steps = suggest_next_steps(comments)
            print(f"[{order_id}] Unresolved - Summary: {summary}, Next Steps: {next_steps}")
            unresolved_data.append([order_id, amount, comments, summary, next_steps])

        else:
            # Step 3: Handle Resolved Cases
            pattern = identify_resolution_pattern(comments)
            if pattern in known_patterns:
                print(f"[{order_id}] Resolved - Auto-closed due to recognized pattern: {pattern}")
                auto_closed = "Yes"
            else:
                print(f"[{order_id}] Resolved - Identified New Pattern: {pattern}")
                auto_closed = "No"
                new_patterns.append(pattern)

            resolved_data.append([order_id, amount, comments, pattern, auto_closed])

    # Step 4: Save unresolved cases
    if unresolved_data:
        unresolved_df = pd.DataFrame(unresolved_data, columns=["Transaction ID", "Amount", "Comments", "Summary", "Next Steps"])
        unresolved_df.to_csv(f"{UNRESOLVED_FOLDER}/unresolved_cases.csv", index=False)

    # Step 5: Save resolved cases
    if resolved_data:
        resolved_df = pd.DataFrame(resolved_data, columns=["Transaction ID", "Amount", "Comments", "Pattern", "Auto Closed"])
        resolved_df.to_csv(f"{RESOLVED_FOLDER}/resolved_cases.csv", index=False)

    # Step 6: Update pattern database
    if new_patterns:
        new_patterns_df = pd.DataFrame({"Pattern": new_patterns})
        new_patterns_df.to_csv(PATTERN_DATABASE, mode='a', header=False, index=False)

    print("Processing completed.")

def main():
    """
    Main function to handle argument parsing and invoke the processing function.
    """
    parser = argparse.ArgumentParser(description="Process resolution data and classify as resolved/unresolved.")
    parser.add_argument('--resolution_file', required=True, help="Path to the resolution CSV file (e.g. data/recon_data_reply.csv).")

    args = parser.parse_args()

    process_resolutions(args.resolution_file)

if __name__ == "__main__":
    main()
