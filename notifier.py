import smtplib
from email.mime.text import MIMEText


class EmailNotifier:

    def __init__(self, sender_email, app_password):
        self.sender_email = sender_email
        self.app_password = app_password

    def send_email(self, receiver_email, subject, body):
        try:
            # Create email message
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = receiver_email

            # Connect to Gmail SMTP server
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)

            print("📧 Email sent successfully!")

        except Exception as e:
            print("❌ Email failed:", e)