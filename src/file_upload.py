import os
import smtplib
import shutil
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import argparse
import pandas as pd

def upload_file(file_path, upload_folder="processed_files"):
    """
    Moves the file to a specified folder.
    If a file with the same name exists, it appends a timestamp to avoid overwriting.

    Args:
    - file_path (str): The path to the file to be uploaded.
    - upload_folder (str): The folder where the file should be uploaded. Defaults to 'processed_files'.
    
    Returns:
    - str: The path where the file was uploaded.
    """
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = os.path.basename(file_path)
    destination_path = os.path.join(upload_folder, filename)

    # Ensure uniqueness by appending a timestamp if a file with the same name exists
    if os.path.exists(destination_path):
        timestamp = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")
        destination_path = os.path.join(upload_folder, f"{timestamp}_{filename}")

    shutil.move(file_path, destination_path)
    print(f"File uploaded to: {destination_path}")
    return destination_path

def send_email(recipient_email, subject, body, attachment_path, smtp_server, smtp_port, sender_email, sender_password):
    """
    Sends an email with an attachment to the specified recipient.

    Args:
    - recipient_email (str): The recipient's email address.
    - subject (str): The subject of the email.
    - body (str): The body content of the email.
    - attachment_path (str): The path to the attachment file.
    - smtp_server (str): The SMTP server address.
    - smtp_port (int): The port number for the SMTP server.
    - sender_email (str): The sender's email address (retrieved from environment variable).
    - sender_password (str): The sender's email password (retrieved from environment variable).

    Returns:
    - None
    """
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    try:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
            msg.attach(part)
    except FileNotFoundError:
        print(f"Error: The attachment file {attachment_path} was not found.")
        return

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email sent to {recipient_email}")
    except smtplib.SMTPException as e:
        print(f"Error: Failed to send email. {e}")

def main():
    """
    Main function to parse arguments, upload the file, and send the email.
    """
    parser = argparse.ArgumentParser(description="Upload processed file and send it via email.")
    parser.add_argument('--file', required=True, help="Path to the file to be uploaded (e.g. data/recon_data_processed.csv).")
    parser.add_argument('--upload_folder', required=False, default="processed_data", help="The folder where the file will be uploaded.")
    parser.add_argument('--email', required=False, help="Recipient email address to send the email to.")

    args = parser.parse_args()

    # Step 1: Upload the file to the specified folder
    uploaded_file = upload_file(args.file, args.upload_folder)

    # # Step 2: Send the email with the uploaded file
    # recipient_email = args.email
    # subject = "Processed Transaction File"
    # body = "Please find the processed transactions file attached."
    
    # # Get SMTP credentials from environment variables
    # sender_email = os.getenv("SMTP_EMAIL")
    # sender_password = os.getenv("SMTP_PASSWORD")
    # smtp_server = os.getenv("SMTP_SERVER", "smtp.example.com")
    # smtp_port = int(os.getenv("SMTP_PORT", "587"))

    # if not sender_email or not sender_password:
    #     raise ValueError("Missing SMTP credentials! Set them as environment variables.")

    # send_email(recipient_email, subject, body, uploaded_file, smtp_server, smtp_port, sender_email, sender_password)

if __name__ == "__main__":
    main()
