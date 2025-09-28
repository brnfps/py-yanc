import time
import logging

from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException, session_log


def conn_config(device, commands, repeat, logger: logging.Logger):
    tries = 0
    while tries < repeat:
        logger.info(f"Connecting to device to send configuration. Trying: { tries + 1 }")
        try:
            with ConnectHandler(**device) as ssh:
                ssh.find_prompt()
                ssh.enable()
                time.sleep(1)
                logger.info(f"Connection successful! Ssending configuration...")
                ssh.send_config_from_file(commands, read_timeout=120)
                ssh.save_config()

                logger.info(f"Configuration sent and saved")
                tries = repeat
                failed = False
        except (NetmikoTimeoutException, NetmikoAuthenticationException, ValueError, Exception) as error:
            logger.error(f"Connection failed: { error }")
            logger.error(f"Retrying...") if tries < repeat - 1 else logger.error("All retries failed.")
            time.sleep(5)
            tries+=1

    if failed:
        raise Exception() 


def conn_timed_config(device, commands, conf_mode, repeat, logger: logging.Logger):
    tries = 0
    while tries < repeat:
        logger.info(f"Connecting to device. Trying: { tries + 1 }")
        try:
            with ConnectHandler(**device) as ssh:
                ssh.enable()
                ssh.config_mode() if conf_mode else None
                logger.info(f"Connection successful! Starting configuration...")
                ssh.send_multiline_timing(commands, read_timeout=90)
                ssh.exit_config_mode

                logger.info(f"Configuration sent")
                tries = repeat
                failed = False
        except (NetmikoTimeoutException, NetmikoAuthenticationException, ValueError, Exception) as error:
            logger.error(f"Connection failed: { error }")
            logger.error(f"Retrying...") if tries < repeat - 1 else logger.error("All retries failed.")
            time.sleep(5)
            tries+=1
            failed = True


    if failed:
        raise Exception()   


def conn_get_prompt(device, repeat, logger: logging.Logger):
    tries = 0
    while tries < repeat:
        logger.info(f"Testing connection... { tries + 1 }")
        try:
            with ConnectHandler(**device) as ssh:
                ssh.find_prompt()
                tries = repeat

                logger.info(f"Connection successful!")
                failed = False
        except (NetmikoTimeoutException, NetmikoAuthenticationException, ValueError, Exception) as error:
            logger.error(f"Connection failed: { error }")
            logger.error(f"Retrying...")
            time.sleep(5)
            tries+=1
            failed = True

    if failed:
        raise Exception()


def main():
   pass


if __name__ == '__main__':
    main()