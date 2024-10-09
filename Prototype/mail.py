import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import requests
import os
import re

# Setup port number and server name

smtp_port = 587  # Standard secure SMTP port
# Mail sent to : treemusketeers32@gmail.com
# Password : Dhootkilillyput
# Mail sent from : spyeyemusk42@gmail.com
# Password : Dhootkilillyput


# Setup port number and server name

smtp_port = 587  # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

# Set up the email lists
email_from = "spyeyemusk42@gmail.com"

# Define the password (better to reference externally)
# As shown in the video this password is now dead, left in as example only
pswd = "ovwx ybbp qdcw ytlf"


def is_valid_url(url):
    # Basic validation regex (can be more strict)
    regex = r"^(http|https)://[^\s]*$"
    return re.match(regex, url) is not None


def secure_open(path):
    if os.path.isfile(path):
        return open(path, 'rb')
    elif is_valid_url(path):
        try:
            response = requests.get(path, stream=True)
            if response.status_code == 200:
                return response.raw
            else:
                print(
                    f"Error: Failed to download file from {path} (Status: {response.status_code})")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: An error occurred while fetching {path}: {e}")
            return None
    else:
        print(f"Invalid path: {path}")
        return None


def send_emails_sale_confirmed(texts, path):

    group_mail = "treemusketeers32@gmail.com"
    hardik_mail = "hardikhpawar.cs21@rvce.edu.in"
    harshit_mail = "harshitdhoot.cs21@rvce.edu.in"
    karan_mail = "karansathish.cs21@rvce.edu.in"

    email_list = [hardik_mail, karan_mail, harshit_mail]

    subject = "Sale Confirmed"

    for person in email_list:
        # Make the body of the email
        body = texts

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))
        filename = path

        attachment = secure_open(filename)  # r for read and b for binary

        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header(
            'Content-Disposition', "attachment; filename= " + filename)
        attachment_package.add_header(
            'Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()

        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print(f"✅ Email sent to: {person}")
        print()

    # Close the port
    TIE_server.quit()


def send_emails_account_created(texts):

    group_mail = "treemusketeers32@gmail.com"
    hardik_mail = "hardikhpawar.cs21@rvce.edu.in"
    harshit_mail = "harshitdhoot.cs21@rvce.edu.in"
    karan_mail = "karansathish.cs21@rvce.edu.in"

    email_list = [hardik_mail, karan_mail, harshit_mail]

    subject = "Account Created"

    for person in email_list:

        # Make the body of the email
        body = texts

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()

        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print(f"✅ Email sent to: {person}")
        print()

    # Close the port
    TIE_server.quit()
