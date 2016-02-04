"""This class execute all neccessary functionality for parsing exchange 
information from web site http://kovalut.ru"""

import requests
import re

class KovalutRuParser:
    
    # Cache
    exchanges_data_cache = {};
    # Url template of exchange info page
    url_template = 'http://kovalut.ru/index.php?kod={code}'
    
    def get_subtext(self, text, mask):
        return re.compile(mask, re.M | re.S).search(text);
        
    
    def get_exchanges_data(self, config):
        """Returns list with exchange info for every bank specified in url 
        http://kovalut.ru/index.php?kod={code}
        Parameter {code} specified in dict cell config['kovalut_ru_code']"""

        # Get result from class cache
        code = config['kovalut_ru_code'];
        if code in KovalutRuParser.exchanges_data_cache:
            return KovalutRuParser.exchanges_data_cache[code]

        # Get exchange information page
        url = KovalutRuParser.url_template.format(code=code);
        page_code = requests.post(url).text

        # Get code on information table
        table_search_result = self.get_subtext(
            page_code, 
            '<table class="tb-k">(.*)<tr id="old-k">'
        )
        
        # If not find - other search
        if not table_search_result:
            table_search_result = self.get_subtext(
                page_code, 
                '<table class="tb-k">(.*)<tr class="ks">'
            )
            
        if not table_search_result:
            return;
        
        # Get all lines info
        p = re.compile(
            '<td class="tbn"><a[^>]*>([^<]*)</a></td>[^<]*'
            '<td[^>]*>([^<]*)</td>[^<]*<td[^>]*>([^<]*)</td>[^<]*'
            '<td[^>]*>([^<]*)</td>[^<]*<td[^>]*>([^<]*)</td>', 
            re.M | re.S
        )
        search_result = p.finditer(table_search_result.group(1));
        if not search_result:
            return;

        # Function for getting float price value from 
        # string value with format XX,XX
        def get_price(string_price):
            'Returns float price from string in format XX,XX'
            return float(string_price.replace(',', '.'));
        
        result_set = [];
        for match in search_result:
            result_set.append({
                'bank_name': match.group(1),
                'USD': {
                    'buy': get_price(match.group(2)), 
                    'sell': get_price(match.group(3)),
                },
                'EUR': {
                    'buy': get_price(match.group(4)), 
                    'sell': get_price(match.group(5)),
                },
            })

        # Put code values into class cache
        KovalutRuParser.exchanges_data_cache[code] = result_set;
        
        return result_set

    def get_best_price_info(self, exchange_data, currency, direction):
        """Search the best price and bank list for specified currency (EUR/USD)
        and direction (buy/sell)"""
        value = 0
        banks = []
        for bank_data in exchange_data:
            current_price = bank_data[currency][direction]
            current_bane_name = bank_data['bank_name']
            # If searched new better price - set new value and clear bank list
            is_for_sell = (direction == 'sell' and current_price < value)
            is_for_buy = (direction == 'buy' and current_price > value)
            if value == 0 or is_for_sell or is_for_buy:
                value = current_price;
                banks = [current_bane_name]
            # If another one best price - ann bank name
            elif value == current_price:
                banks.append(current_bane_name)

        return {
            'price': value,
            'banks': banks,
        }