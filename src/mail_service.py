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

# receiver_email = "ziemi.siema@gmail.com"


def SendConfirmation(receiver, hash):

    message = MIMEMultipart("alternative")
    message["Subject"] = "Account Verification"
    message["From"] = f"Learn!T <{sender_email}>"
    message["To"] = receiver

    text = f"""\
    Hello,
    Your activation link:
    {os.getenv('LOCALHOST')+"confirmation?pass="+hash}
    If you didn't create new account on our site, ignore that message.
    """

    html = f"""\
    <html>
    <head>
        <style>
            .bar {{height: 50px;width: 100%;background-color: #212529;text-align: center;font-weight: bold;color: white;}}
            .text {{line-height: 50px;height: 100%;color:white;}}
            .mailBody{{justify-content: center;text-align: center;}}
            a {{font-weight: bold;color: green;}}
            .ignorant{{font-size: x-small;}}
        </style>
    </head>
    <body>
        <div class='bar'>
            <div class='text'>Learn!T</div>
        </div>
        <div class="mailBody">
            <p>
                Hello,<br>
                Your activation link:<br>
                <div><a href="{os.getenv('LOCALHOST')+"confirmation?pass="+hash}">ACTIVATE ACCOUNT</a></div>
            </p>
            <div class="ignorant">
                If you didn't create new account on our site, ignore that message.
            </div>
        </div>
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
        server.sendmail(sender_email, receiver, message.as_string())


def SendRecovery(receiver, hash):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Account Verification"
    message["From"] = f"Learn!T <{sender_email}>"
    message["To"] = receiver

    text = f"""\
    Hello,
    Your activation link:
    {os.getenv('LOCALHOST')+"recover?pass="+hash}
    If you didn't request reset, ignore that message.
    """

    html = f"""\
    <html>
    <head>
        <style>
            .bar {{height: 50px;width: 100%;background-color: #212529;text-align: center;font-weight: bold;color: white;}}
            .text {{line-height: 50px;height: 100%;color:white;}}
            .mailBody{{justify-content: center;text-align: center;}}
            a {{font-weight: bold;color: green;}}
            .ignorant{{font-size: x-small;}}
        </style>
    </head>
    <body>
        <div class='bar'>
            <div class='text'>Learn!T</div>
        </div>
        <div class="mailBody">
            <p>
                Hello,<br>
                Your reset link:<br>
                <div><a href="{os.getenv('LOCALHOST')+"recover?pass="+hash}">RESET PASSWORD</a></div>
            </p>
            <div class="ignorant">
                If you didn't request reset, ignore that message.
            </div>
        </div>
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
        server.sendmail(sender_email, receiver, message.as_string())
