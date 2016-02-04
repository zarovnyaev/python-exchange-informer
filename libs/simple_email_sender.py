"""This class used for email letters simple sending"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SimpleEmailSender:
    
    @staticmethod
    def send(parameters):
        # Generation information of sender
        from_info = SimpleEmailSender.get_email('from_email', 'from_name', 
                                                parameters)
        # Generation information of receiver
        to_info = SimpleEmailSender.get_email('to_email', 'to_name', 
                                              parameters)
        # Get server data
        server = parameters['server']
        port = parameters['port']
        username = parameters['username']
        password = parameters['password']
        # Get email data
        text = parameters['text']
        subject = parameters['subject']
        
        # Message headers
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = from_info
        msg['To'] = to_info
        msg.attach(MIMEText(text, 'plain'))

        # Server connect and authorization
        s = smtplib.SMTP(server, port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(username, password)
        
        # Sending
        s.sendmail(from_info, to_info, msg.as_string())
        s.quit()
    
    @staticmethod
    def get_email(email_cell, name_cell, data):
        if not email_cell in data:
            return ''
        elif not name_cell in data:
            return data[email_cell]
        else:
            return "{0} <{1}>".format(data[name_cell], data[email_cell])        