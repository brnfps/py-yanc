import yaml
import os

from jinja2 import Environment, FileSystemLoader

def yaml_to_dict(yaml_file):
    with open(yaml_file, 'r') as file:
        config_dict = yaml.safe_load(file)
    return config_dict

def gen_config(yaml_file):
    config = yaml_to_dict(yaml_file)

    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('templates/vios.j2')
    
    rendered_config = template.render(config)

    return config, rendered_config

def main():
    pass

if __name__ == '__main__':
    main()