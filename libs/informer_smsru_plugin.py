"""This plugin executes "SmsRu" information process. 
This process sende SMS on the receiver cellphone using sms.ru account.

Config parameters:

[RECEIVER_1]
name = Test_Debug
informer_type = smsru
informer_api_id = API ID FROM SMS.RU ACCOUNT
informer_phone_number = +12345678901
informer_text_template = 1 {currency} = {new_price} rub. ({chenged} rub.). Banks: {bank_list}.
kovalut_ru_code = AREA CODE FROM SITE KOVALUT.RU
currency = USD/EUR
direction = buy/sell
last_price = 0
last_message = 
"""

from libs.inform_text import InformText
import urllib.parse
import requests

class InformerSmsruPlugin:
    
    @staticmethod
    def inform(best_price_info, config):
        
        api_id = config['informer_api_id']
        to = config['informer_phone_number']
        text = InformText.get_text(config['informer_text_template'], 
                                   best_price_info, 
                                   config)

        # Check if sms text was not changed - not send new message
        if text == config['last_message'] or \
           best_price_info['price'] == config['last_price']:
            return
        
        # Generation of request url for sending the sms
        get_parameters = urllib.parse.urlencode({'api_id': api_id,
                                                 'to': to,
                                                 'text': text})

        url = 'http://sms.ru/sms/send?' + get_parameters

        # Send
        requests.post(url)
        
        # Set new last information parameters in config
        config['last_message'] = text
        config['last_price'] = str(best_price_info['price'])