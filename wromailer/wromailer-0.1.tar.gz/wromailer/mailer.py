import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import getpass
import os


class Mailer():

    def __init__(self, login, subject, template_file, assistant_template_file):
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        self.mailServer = mailServer
        self.login = login
        self.subject = subject
        if not os.path.exists(template_file):
            raise Exception("Template file not found at '%s'" % template_file)
        with open(template_file, encoding='utf8') as f:
            self.template = f.read()
        if not os.path.exists(assistant_template_file):
            raise Exception("Template file not found at '%s'" % assistant_template_file)
        with open(assistant_template_file, encoding='utf8') as f:
            self.template_assistant = f.read()
        if not 'GMAIL_PASS' in os.environ:
            pswd = getpass.getpass("GMail password for username '%s', please...\n" % login)
        else:
            pswd = os.environ['GMAIL_PASS']
        mailServer.login(self.login, pswd)

    def close_mailer(self):
        self.mailServer.close()

    def send_email(self, ical, mailto, name, assistant, assignment_time, task_name, lesson):
        attendees = [mailto]
        fro = self.login
        subject = self.subject
        assistant = assistant
        assignment_date_text = assignment_time.strftime('%Y-%m-%d')
        email_body = self.template % (name, assistant, assignment_date_text, task_name, lesson)
        ## the same
        msg = MIMEMultipart('mixed')
        msg['Reply-To']=fro
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg['From'] = fro
        msg['To'] = ",".join(attendees)
        part_email = MIMEText(email_body,"html")
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)
        if ical:
            part_cal = MIMEText(ical.decode("utf-8") ,'calendar;method=REQUEST')
            ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
            ical_atch.set_payload(ical)
            encoders.encode_base64(ical_atch)
            ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))
            msgAlternative.attach(part_cal)
        msgAlternative.attach(part_email)
        answer = input('Should I send REGULAR email to %s (address %s)? date %s, taskname %s? [y/n]\n' % (name, attendees, assignment_date_text, task_name))
        if answer == 'y':
            self.mailServer.sendmail(fro, attendees, msg.as_string())
        else:
            print('-' * 40)
            print('Aborting for %s...! Mail not send!!' % attendees)
            print('-' * 40)   
            print(' ')   

    def send_email_assistant(self, ical, mailto, name, assistant, assignment_time, task_name):
        if not mailto:
            raise Exception("Mailto is empty for assistant %s!" % assistant)
        attendees = [mailto]
        fro = self.login
        subject = self.subject
        assignment_date_text = assignment_time.strftime('%Y-%m-%d')
        email_body = self.template_assistant % (assistant, name, assignment_date_text, task_name)
        ## the same
        msg = MIMEMultipart('mixed')
        msg['Reply-To']=fro
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject + ' [Assistant]'
        msg['From'] = fro
        msg['To'] = ",".join(attendees)
        part_email = MIMEText(email_body,"html")
        part_cal = MIMEText(ical.decode("utf-8") ,'calendar;method=REQUEST')
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)
        ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
        ical_atch.set_payload(ical)
        encoders.encode_base64(ical_atch)
        ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))
        msgAlternative.attach(part_email)
        msgAlternative.attach(part_cal)
        answer = input('Should I send ASSISTANT email to %s (address %s) ? time %s taskname %s [y/n]\n' % (assistant, attendees, assignment_date_text, task_name))
        if answer == 'y':
            self.mailServer.sendmail(fro, attendees, msg.as_string())
        else:
            print('Aborting for %s...' % attendees)