import os
import time

from connector import conn_config, conn_timed_config, conn_get_prompt
from config import gen_config
from deployment.deployment import deployment



VERSION = "0.0.2-alpha-1"


def generate_config(yaml_file): 
    yaml_dict = gen_config(yaml_file)
    return yaml_dict


# def zeroize(device):
#     commands = [
#         'erase startup-config',
#         'reload',
#         'y'
#     ]
#     conn_timed_config(device['device'], commands, None, 300)


def main():
    """
    The main idea of this software is to receive a yaml file with device's configuration,
    generates a <hostname>.cfg file for configuration version control and, from this file,
    configure the device. (Future versions - want to add a unique identifier to the files
    and support other imports [json|xml|csv])

    Since the code works in a for loop, it can deploy more than one device per run, 
    but executes it one by one. (Maybe in a far future, asyncio/multithread may be considered)

    It has the following sequency:
    - Generates configuration from yaml file
    - Check if device needs to be zeroized
    - Test device's connection (ssh|telnet)
    - Disable logging to avoid unwanted messages that could break the code
    - Set the hostname to avoid prompt issues while running send_config_from_file
    - Send config from file
    """
    deployment()

    # zeroizing = False  # Set to True if you want to zeroize the device before configuration
        
    #     if zeroizing is True:
    #         print("Zeroizing device")
    #         zeroize(yaml_dict)
    #         print("Device reseted to factory default")
    #         time.sleep(30)


if __name__ == '__main__':
    main()