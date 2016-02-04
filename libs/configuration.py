
import configparser
import os

class Configuration:
    
    config = None
    config_file_path = "config.ini"
    
    @staticmethod
    def get_config_path():
        return os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] \
            + '/' + Configuration.config_file_path;
        
    @staticmethod
    def get():
        """Returns configuration object"""
        if Configuration.config == None:
            Configuration.config = configparser.ConfigParser()
            Configuration.config.read(Configuration.get_config_path())
        return Configuration.config
    
    @staticmethod
    def get_category(category_name):
        """Returns specified category's parameters dict"""
        if category_name in Configuration.get():
            return Configuration.get()[category_name]
        else:
            return None
    
    @staticmethod
    def save():
        """Save configuration to the file"""
        with open(Configuration.get_config_path(), 'w') as configfile:
            Configuration.get().write(configfile)        
    