import smtplib
from email.mime.text import MIMEText

def sendEmail(sender_email, app_password, receiver_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"
