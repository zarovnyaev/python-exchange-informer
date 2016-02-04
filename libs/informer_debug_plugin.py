"""This plugin executes "Debug" information process. 
This process just shows information string in console.

Config parameters:

[RECEIVER_1]
name = Test_Debug
informer_type = debug
informer_text_template = 1 {currency} = {new_price} rub. ({chenged} rub.). Banks: {bank_list}.
kovalut_ru_code = AREA CODE FROM SITE KOVALUT.RU
currency = USD/EUR
direction = buy/sell
last_price = 0
last_message = 
"""

from libs.inform_text import InformText

class InformerDebugPlugin:
    
    @staticmethod
    def inform(best_price_info, config):
        
        text = InformText.get_text(config['informer_text_template'], 
                                   best_price_info, 
                                   config)

        print(text)
        
        # Set new last information parameters in config
        config['last_price'] = str(best_price_info['price'])        