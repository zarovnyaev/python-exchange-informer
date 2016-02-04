"""This plugin executes "Console" information process. 
This process executes console command with information.

Config parameters:

[RECEIVER_1]
name = Test_Console
informer_type = console
informer_command_template = notify-send "Exchange Informer" "1 {currency} = {new_price} rub. ({chenged} rub.). Banks: {bank_list}." -i gtk-dialog-info
kovalut_ru_code = AREA CODE FROM SITE KOVALUT.RU
currency = USD/EUR
direction = buy/sell
last_price = 0
last_message = 
"""

from libs.inform_text import InformText
import os

class InformerConsolePlugin:
    
    @staticmethod
    def inform(best_price_info, config):
        
        command = InformText.get_text(config['informer_command_template'], 
                                      best_price_info, 
                                      config)

        # Check if sms text was not changed - not send new message
        if command == config['last_message'] or \
           best_price_info['price'] == config['last_price']:
            return

        os.system(command);

        # Set new last information parameters in config
        config['last_message'] = command
        config['last_price'] = str(best_price_info['price'])