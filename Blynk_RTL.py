import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Email configuration
sender_email = 'rtllab55@gmail.com'
sender_password = os.environ.get('SENDER_EMAIL_PASSWORD')
receiver_emails = ['nageshwalchtwar257@gmail.com', 'akshit.gureja@research.iiit.ac.in', 'rishabh.agrawal@students.iiit.ac.in']
mail_server = 'smtp.gmail.com'  
mail_port = 587

def get_res():
    url = "https://blr1.blynk.cloud/external/api/get?token=vTZNEt9WyE--pOBu6LmH_QMAkoEcC4hd&v3"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    on_btn = response.text
    return on_btn

def send_email(subject, body, receivers):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receivers)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(mail_server, mail_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receivers, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

prev_status = '0'  # Initializing previous status as '0'

while True:
    status = get_res()

    if status != prev_status:  # If there's a change in status, log the timestamp to README
        with open("README.md", "a") as file:
            if status == '1':
                file.write(f"- Button Usage pressed at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            else:
                file.write(f"- Experiment is not in use at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        prev_status = status  # Update previous status with the current status

    current_time = time.strftime('%H:%M')
    if current_time == '00:00':
        # Send email at 00:00 (midnight) every day
        with open("README.md", "r") as file:
            log_content = file.read()
            send_email("Button Usage Log of VR - RTL", log_content, receiver_emails)

    time.sleep(1)
