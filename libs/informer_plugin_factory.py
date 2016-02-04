"""This is class factory form informer plugins"""

class InformerPluginFactory:
    
    @staticmethod
    def inform(best_price_info, config):
        """Execute informer plugin's specified in 
        dict cell config['informer_type']"""
        informer = InformerPluginFactory.get_informer_plugin(config['informer_type'])
        informer.inform(best_price_info, config)
        
    @staticmethod
    def get_informer_plugin(type):
        """Returns plugin class object"""
        module = __import__('libs.informer_' + type + '_plugin', fromlist=[''])
        return getattr(module, 'Informer' + type.capitalize() + 'Plugin')