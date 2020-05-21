import os
import requests, urllib
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "Resume - {}"
body = "Greetings from Resume Generator!\n\nPFA a shareable link to your resume along with your resume file.\n{}\nThank you\nAutomated Resume Generator"
sender_email = "resumegeneratorpes@gmail.com"
password = "dbmspes123"
url = r"https://script.google.com/macros/s/AKfycbxDUQuHHMayj191-E2GZVQXwu0PUrM1UUdksFN_q0_UdnSfrlfi/exec?"

def send_resume(name, receiver_email, doc_name, resume_url):
    print("Sending resume......",end="")
    message = MIMEMultipart()
    message["From"] = "Automated Resume Generator <resumegeneratorpes@gmail.com>"
    message["To"] = receiver_email
    message["Subject"] = subject.format(name)
    message.attach(MIMEText(body.format(resume_url), "plain"))
    with open(doc_name, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)

    part.add_header("Content-Disposition", f"attachment; filename= {doc_name}")

    message.attach(part)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    print("sent!")

def create_resume(items):
    print("Creating resume......", end = "")
    new_url = url + urllib.parse.urlencode(items)
    response = requests.get(new_url)
    resume_url = response.content
    resume_pdf = requests.get(resume_url)
    doc_name = "{}.pdf".format(items["name"])
    with open(doc_name, "wb") as f:
        f.write(resume_pdf.content)
    print("Created!")
    send_resume(items["name"],items["email"],doc_name,resume_url)
