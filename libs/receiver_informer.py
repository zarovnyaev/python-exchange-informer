"""This class execute informing process for the receiver with configuration 
specified in self.config with __init__ function"""

from libs.informer_plugin_factory import InformerPluginFactory
from libs.kovalut_ru_parser import KovalutRuParser

class ReceiverInformer:
    
    def __init__(self, config):
        self.config = config
        
    def inform(self):
    
        # If receiver want sell currency we must parse bank buying info
        direction = 'sell'
        if self.config['direction'] == 'sell':
            direction = 'buy'
        
        # Get the best price and bank list
        data_parser = KovalutRuParser();
        best_price_info = data_parser.get_best_price_info(
            data_parser.get_exchanges_data(self.config), 
            self.config['currency'], 
            direction
        );
        
        # Inform
        InformerPluginFactory.inform(
            config=self.config,
            best_price_info=best_price_info,
        );
        