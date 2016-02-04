"""This plugin executes "Email" information process. 
This process sends email with information.

Config parameters:

[RECEIVER_1]
name = Test_Email
informer_type = email
informer_subject_template = New currency exchange information
informer_text_template = 1 {currency} = {new_price} rub. ({chenged} rub.). Banks: {bank_list}.
informer_email = RECEIVER@EMAIL.COM
informer_email_name = RECEIVER
kovalut_ru_code = AREA CODE FROM SITE KOVALUT.RU
currency = USD/EUR
direction = buy/sell
last_price = 0
last_message = 

[SMTP_SERVER]
server = SENDER.SMTP.SERVER.URL
port = PORT NUMBER
name = SENDER NAME
email = SENDER@EMAIL.COM
username = SENDER
password = Qwerty1
"""

from libs.inform_text import InformText
from libs.simple_email_sender import SimpleEmailSender
from libs.configuration import Configuration

class InformerEmailPlugin:
    
    @staticmethod
    def inform(best_price_info, config):
        
        text = InformText.get_text(config['informer_text_template'], 
                                   best_price_info, 
                                   config)
        
        subject = InformText.get_text(config['informer_subject_template'], 
                                      best_price_info, 
                                      config)

        # Check if sms text was not changed - not send new message
        if text == config['last_message'] or \
           best_price_info['price'] == config['last_price']:
            return

        server_config = Configuration.get_category('SMTP_SERVER');

        SimpleEmailSender.send({'to_email': config['informer_email'],
                                'to_name': config['informer_email_name'],
                                'server': server_config['server'],
                                'port': server_config['port'],
                                'username': server_config['username'],
                                'password': server_config['password'],
                                'from_email': server_config['email'],
                                'from_name': server_config['name'],
                                'text': text,
                                'subject': subject})

        # Set new last information parameters in config
        config['last_message'] = text
        config['last_price'] = str(best_price_info['price'])