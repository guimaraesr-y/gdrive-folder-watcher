import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GmailService:
    def __init__(self, email, app_password):
        self.email = email
        self.app_password = app_password

    def send_message(self, to: str, subject: str, message_text: str, files: str = None):
        """Send an email message using the Gmail SMTP server."""
        msg = MIMEMultipart()
        msg["From"] = self.email
        msg["To"] = to
        msg["Subject"] = subject

        msg.attach(MIMEText(message_text))

        # Attach files if provided
        if files:
            for file in files:
                with open(file, "rb") as f:
                    attachment = MIMEBase("application", "octet-stream")
                    attachment.set_payload(f.read())

                encoders.encode_base64(attachment)
                attachment.add_header(
                    "Content-Disposition", f"attachment; filename= {file}"
                )

                msg.attach(attachment)

        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()  # Identify ourselves to an SMTP server
            smtp.starttls()  # Secure our email with tls encryption
            smtp.ehlo()  # Re-identify ourselves as an encrypted connection

            smtp.login(self.email, self.app_password)
            smtp.send_message(msg)
            smtp.quit()
