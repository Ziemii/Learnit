import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from dotenv import load_dotenv
import os

load_dotenv()

sender_email = os.getenv('SENDER')
SMTPhost = os.getenv('HOST')
password = os.getenv('MAILSSWORD')
port = os.getenv('PORT')

receiver_email = "ziemi.siema@gmail.com"

def SendConfirmation(receiver, hash):

    message = MIMEMultipart("alternative")
    message["Subject"] = "Account Verification"
    message["From"] = f"Learn!T <{sender_email}>"
    message["To"] = receiver

    text = f"""\
    Hi,
    How are you?
    Your confirmation: {hash}
    www.realpython.com"""


    html = f"""\
    <html>
    <body>
        <p>Hi,<br>
        How are you?<br>
        <a href="{os.getenv('LOCALHOST')+"confirmation?pass="+hash}">Your confirmation</a><br>
        {os.getenv('LOCALHOST')+"confirmation/?pass="+hash}
         
        has many great tutorials.
        </p>
    </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")  
    message.attach(part1)
    message.attach(part2)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTPhost, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def SendRecovery(receiver, hash):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Account Verification"
    message["From"] = f"Learn!T <{sender_email}>"
    message["To"] = receiver

    text = f"""\
    Hi,
    How are you?
    Your confirmation: {hash}
    www.realpython.com"""


    html = f"""\
    <html>
    <body>
        <p>Hi,<br>
        Below you can reset your password<br>
        <div> </div>
        <a href="{os.getenv('LOCALHOST')+"recover?pass="+hash}">RESET</a><br>
         
        </p>
    </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")  
    message.attach(part1)
    message.attach(part2)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTPhost, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())