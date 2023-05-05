import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Setup port number and server name
smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

# Set up the email lists
email_from = "example@gmail.com"
email_list = ["recipient1@gmail.com", "recipient2@gmail.com"]

# Define the password (better to reference externally)
pswd = "psw.txt"

# Name the email subject
subject = "New email from me with attachments!!"

# Define the email function (don't call it email!)
def send_emails(email_list):

    filename = ''

    for person in email_list:
        # Make the body of the email
        body = f"""
        Hi there,

        Please see the attached file: {filename}

        Best regards,
        Me
        """

        # Make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Iterate over files in the directory and attach them to the email
        folder_path = r"C:\path\to\folder"
        for filename in os.listdir(folder_path):
            attachment_path = os.path.join(folder_path, filename)
            if os.path.isfile(attachment_path):
                attachment = open(attachment_path, "rb")
                # Encode as base 64
                attachment_package = MIMEBase('application', 'octet-stream')
                attachment_package.set_payload(attachment.read())
                encoders.encode_base64(attachment_package)
                attachment_package.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(attachment_package)

        # Attach the body of the message
        msg.attach(MIMEBase('text', 'plain'))
        body_part = MIMEBase('text', 'plain')
        body_part.set_payload(body)
        msg.attach(body_part)

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Successfully connected to server")
        print()

        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

        # Close the attachment
        attachment.close()

    # Close the port
    TIE_server.quit()

# Run the function
send_emails(email_list)
