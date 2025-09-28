import logging

def custom_logger(log_name, hostname):
    logger = logging.getLogger(f"{ __name__ }:{ log_name.split('.')[0] }:{ hostname }")
    logger.setLevel(logging.DEBUG)

    format_string = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_format = logging.Formatter(format_string, datefmt='%Y-%m-%d %H:%M:%S %z')

    file_handler = logging.FileHandler(hostname + '.log', mode='w')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger


def remove_handlers(logger: logging.Logger):
    for handler in logger.handlers[:]:
        logger.info("Deployment finished!")
        logger.removeHandler(handler)