import smtplib
import imghdr
import os
from email.message import EmailMessage

from dotenv import load_dotenv
load_dotenv()


EMAIL_SENDER = os.getenv("GMAIL_USERNAME")
EMAIL_RECEIVER = os.getenv("GMAIL_USERNAME")

def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New object appeared"
    email_message.set_content("Hey, we detected an object moving in your camera")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(EMAIL_SENDER, os.getenv("GMAIL_APP_PASSWORD"))
    gmail.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == '__main__':
    send_email(image_path="images/1.png")