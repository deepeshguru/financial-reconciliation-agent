import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Financial Reconciliation Agent")
    parser.add_argument("--step", choices=["preprocessing", "upload", "resolution"], required=True, help="Choose a step to execute")

    args = parser.parse_args()

    if args.step == "preprocessing":
        os.system("python src/preprocessing.py --input data/recon_data_raw.csv --output data/recon_data_processed.csv")
    elif args.step == "upload":
        os.system("python src/file_upload.py --file data/recon_data_processed.csv")
    elif args.step == "resolution":
        os.system("python src/resolution_handling.py --resolution_file data/resolution_data.csv")

if __name__ == "__main__":
    main()
