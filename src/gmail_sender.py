import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import os


def send_email_with_json_and_image(
    sender_email: str,
    sender_password: str,
    recipient_email: str,
    extracted_json: dict,
    image_path: str
):
    """
    Sends an email with a JSON attachment and an image attachment.

    Args:
        sender_email (str): Your Gmail address
        sender_password (str): Your Gmail app password
        recipient_email (str): Recipient's Gmail address
        extracted_json (dict): Extracted car listing JSON
        image_path (str): Path to the car image
    """

    # Create message container
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "Car Listing Data + Image"

    # Add body text
    body = "Please find attached the extracted car listing JSON and the uploaded car image."
    msg.attach(MIMEText(body, "plain"))

    # Attach JSON file
    json_str = json.dumps(extracted_json, indent=4)
    json_attachment = MIMEApplication(json_str, Name="car_listing.json")
    json_attachment["Content-Disposition"] = 'attachment; filename="car_listing.json"'
    msg.attach(json_attachment)

    # Attach Image (if provided)
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            mime = MIMEBase("image", "jpeg", filename=os.path.basename(image_path))
            mime.add_header("Content-Disposition", "attachment", filename=os.path.basename(image_path))
            mime.add_header("X-Attachment-Id", "0")
            mime.add_header("Content-ID", "<0>")
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)

    # Send Email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)  # Use App Password here
            server.send_message(msg)

        print("✅ Email sent successfully!")

    except Exception as e:
        print("❌ Failed to send email:", str(e))

# tested the module and it worked successfully
# sender_email = 
# sender_password = 
# recipient_email = 
# extracted_json = {}
# image_path = 
# send_email_with_json_and_image(sender_email, 
#                                sender_password, 
#                                recipient_email, 
#                                extracted_json,
#                                image_path)