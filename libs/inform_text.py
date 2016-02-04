
class InformText:
    
    @staticmethod
    def get_text(template, best_price_info, config):
        """Implements information from best_price_info and config dicts 
        into template"""
        
        new_price = float(best_price_info['price'])
        
        if (config['last_price'] == ''):
            config['last_price'] = '0'
        last_price = float(config['last_price'])
        
        chenged = float(round(new_price - last_price, 2))
        if chenged >= 0: 
            chenged = '+' + str(chenged)
        
        replacement = {'currency': config['currency'],
                       'new_price': new_price,
                       'bank_list': ', '.join(best_price_info['banks']),
                       'chenged': chenged,
                       'name': config['name']}
        
        return template.format(**replacement)