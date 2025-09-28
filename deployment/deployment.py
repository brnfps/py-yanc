import os
import time


from connector import conn_config, conn_timed_config, conn_get_prompt
from config import gen_config
import core.logger as cl


MAIN_FOLDER = "deployment/to_deploy/"
DEPLOYED_FOLDER = "deployment/deployed/"


def deployment():
    # Collecting all YAML files in the MAIN_FOLDER
    yaml_files = [os.path.join(MAIN_FOLDER, f) for f in os.listdir(MAIN_FOLDER) if f.endswith('.yaml') or f.endswith('.yml')]

    for yaml_file in yaml_files:
        yaml_dict, rendered_config = gen_config(yaml_file)
        
        # Validates if config was successfully read in a dictionary, this is a must.
        try:
            if yaml_dict['device']:
                pass
        except KeyError:
            print("ERROR: No device connection info found in the YAML file.")
            break

        print(yaml_dict["hostname"])
        print("---" * 20)

        # Creates the main directory of the loop ("deployed/<hostname>"), where all the files related to that deployment will be stored. This is a must.
        try:
            os.makedirs(f"{DEPLOYED_FOLDER}/{ yaml_dict['hostname'] }", exist_ok=True)
            main_folder = f"{DEPLOYED_FOLDER}{ yaml_dict['hostname'] }/"
        except Exception as e:
            print(f"Failed to create directory for {yaml_dict['hostname']}: {e}")   
            break
        
        # Setup logger and start deployment
        logger = cl.custom_logger(f"{__name__}:{yaml_dict["hostname"]}", main_folder + yaml_dict["hostname"])
        
        logger.info(f"Starting deployment of {yaml_dict["hostname"]}")
        logger.info(f"Generating configuration file for {yaml_dict["hostname"]}")
        
        # Write config into a file
        cfg_file = f"{ main_folder }{ yaml_dict['hostname'] }.cfg"
        try:
            with open(cfg_file, 'w') as file:
                file.write(rendered_config)

            logger.info(f"Configuration file saved to { main_folder }{yaml_dict['hostname']}.cfg")
        except Exception as e:
            logger.error(f"Failed to create directory or write config file for {yaml_dict['hostname']}: {e}")
            break
        
        # Testing connection
        logger.info(f"Testing connection to {yaml_dict['hostname']}")
        try:
            conn_get_prompt(yaml_dict['device'], 5, logger)
            logger.info(f"Connection test DONE")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Connection test failed for {yaml_dict['hostname']}: {e}")
            logger.error("Deployment failed. Please check the connectivity with device")
            cl.remove_handlers(logger)
            break

        # Disabling terminal logging and setting hostname
        logger.info(f"Disabling terminal logging and setting hostname for {yaml_dict['hostname']}")
        try:
            hostname = yaml_dict['hostname']

            commands = [
                'no ip domain-lookup',
                'no logging console',
                f'hostname { hostname }'
            ]

            conn_timed_config(yaml_dict['device'], commands, True, 3, logger)
            logger.info(f"Terminal logging disabled and hostname set to {hostname}")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to disable terminal logging or set hostname for {yaml_dict['hostname']}: {e}")
            logger.error("Deployment failed. Please check the connectivity with device")
            cl.remove_handlers(logger)
            break

        # Sending configuration file
        logger.info(f"Sending configuration file to {yaml_dict['hostname']}")
        try:
            conn_config(yaml_dict['device'], cfg_file, 5, logger)
            logger.info(f"Device {yaml_dict['hostname']} configured successfully")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to send configuration file to {yaml_dict['hostname']}: {e}")
            logger.error("Deployment failed. Please check the connectivity with device")
            cl.remove_handlers(logger)
            break

        logger.info(f"Deployment of {yaml_dict['hostname']} completed successfully")
        cl.remove_handlers(logger)


def main():
   pass


if __name__ == '__main__':
    main()