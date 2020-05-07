import sys
import smtplib
import datetime
from pathlib import Path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


def mail(svc, status, hostname, email, login_pass):
    """ A module for sending email alerts """
    #my_file = Path(file)
    #if my_file.is_file():
    now = datetime.datetime.now()
    fromadd = 'rimsd.filesend@rimschools.org'
    toadd = email
    message = (f"The service {svc} on {hostname} is {status}")

    msg = MIMEMultipart()
    msg['From'] = fromadd
    msg['To'] = toadd
    msg['Subject'] = message

    body = 'This is an automated message'
    #part = MIMEBase('application', "octet-stream")
    #part.set_payload(open(my_file.name, "rb").read())
    #encoders.encode_base64(part)
    #part.add_header('Content-Disposition', 'attachment; filename={0}'.format(my_file.name))
    #msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromadd, login_pass)
    text = msg.as_string()
    server.sendmail(fromadd, toadd, text)
    server.quit()
    #else:
     #   print("Can't find the file %s" % (file))

