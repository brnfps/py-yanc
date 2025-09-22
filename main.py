import os
import time

from connector import conn_config, conn_timed_config, conn_get_prompt
from config import gen_config


VERSION = "0.0.1-alpha-1_MVP"


def generate_config(yaml_file): 
    yaml_dict = gen_config(yaml_file)
    return yaml_dict


def zeroize(device):
    commands = [
        'erase startup-config',
        'reload',
        'y'
    ]
    conn_timed_config(device['device'], commands, None, 300)


def test_connection(device):  
    conn_get_prompt(device, 20)


def disable_terminal_logging(device):
    hostname = device['hostname']

    commands = [
        'no ip domain-lookup',
        'no logging console',
        f'hostname { hostname }'
    ]

    conn_timed_config(device['device'], commands, True, 3)

def send_config(device, config_file):
    conn_config(device['device'], config_file)


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

    zeroizing = False

    to_deploy = os.listdir("to_deploy")

    for each in to_deploy:
        device_yaml_file = os.path.join("to_deploy", each)
        print(f"1. Deploying {each.split('.')[0]}")
        yaml_dict = generate_config(device_yaml_file)

        try:
            if yaml_dict['device']:
                print(f"2. Configuration generated for {yaml_dict['hostname']}")
                print(f"   And file saved to created/{yaml_dict['hostname']}.cfg")
        except KeyError:
            print("ERROR: No device connection info found in the YAML file.")
            break
        
        if zeroizing is True:
            print("Zeroizing device")
            zeroize(yaml_dict)
            print("Device reseted to factory default")
            time.sleep(30)

        print(f"3. Connecting and configuring {yaml_dict['hostname']}")
        print(f"3.1 Testing connection")
        test_connection(yaml_dict['device'])
        print(f"3.1 DONE")
        time.sleep(3)

        print("3.2 Disabling terminal login and setting hostname")
        disable_terminal_logging(yaml_dict)
        print(f"3.2 DONE")

        time.sleep(5)
        print("3.3 Sending configuration file")
        send_config(yaml_dict, f"created/{yaml_dict['hostname']}.cfg")
        print("3.3 DONE")
        print("4. Configuration DONE")
        print("-" * 40)
        time.sleep(10)


if __name__ == '__main__':
    main()