#!/usr/bin/env python3

from libs.receiver_informer import ReceiverInformer
from libs.configuration import Configuration

# Get config
config = Configuration.get()

# Going thru receivers and process all
receiver_number = 1
receiver_config_param_name = "RECEIVER_{0}"
while(receiver_config_param_name.format(receiver_number) in config):
    # Receiver config group name
    receiver_config_group = receiver_config_param_name.format(receiver_number)
    # Notifing
    receiveNotifier = ReceiverInformer(config[receiver_config_group]);
    receiveNotifier.inform();
    # Receiver number incrementing
    receiver_number += 1
    
# Save new values to the config
Configuration.save()
