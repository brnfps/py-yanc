import logging
import time
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException, session_log



logging.basicConfig(filename=f'logs/netmiko/{time.time()}.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")


def conn_config(device, commands):
    print("-- Connecting to device...")
    tries = 0
    while tries < 3:
        print(f"--- Trying { tries + 1}")
        try:
            with ConnectHandler(**device) as ssh:
                ssh.find_prompt()
                ssh.enable()
                time.sleep(1)
                ssh.send_config_from_file(commands, read_timeout=120)
                ssh.save_config()

                print("--- Config sent")
                tries = 3
        except (NetmikoTimeoutException, NetmikoAuthenticationException, ValueError, Exception) as error:
            time.sleep(5)
            tries+=1


def conn_timed_config(device, commands, conf_mode, repeat):
    print("-- Connecting to device...")
    tries = 0
    while tries < repeat:
        print(f"---- Trying { tries + 1}")
        try:
            with ConnectHandler(**device) as ssh:
                ssh.enable()
                ssh.config_mode() if conf_mode else None
                ssh.send_multiline_timing(commands, read_timeout=90)
                ssh.exit_config_mode

                print("--- Config sent")
                tries = repeat
        except (NetmikoTimeoutException, NetmikoAuthenticationException, ValueError, Exception) as error:
            time.sleep(5)
            tries+=1


def conn_get_prompt(device, repeat):
    tries = 0
    while tries < repeat:
        print(f"---- Trying { tries + 1}")
        try:
            with ConnectHandler(**device) as ssh:
                ssh.find_prompt()
                tries = repeat
        except (NetmikoTimeoutException, NetmikoAuthenticationException, ValueError, Exception) as error:
            time.sleep(5)
            tries+=1


def main():
   pass


if __name__ == '__main__':
    main()