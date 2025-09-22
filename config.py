import yaml

from jinja2 import Environment, FileSystemLoader

def yaml_to_dict(yaml_file):
    with open(yaml_file, 'r') as file:
        config_dict = yaml.safe_load(file)
    return config_dict

def gen_config(yaml_file):
    main_folder = "created/"

    config = yaml_to_dict(yaml_file)

    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('templates/vios.j2')

    # This line was left here because, for any reason that I didn't look into yet,
    # 
    # config = config_dict
    
    rendered_config = template.render(config)
    
    with open(f"{ main_folder }{ config['hostname'] }.cfg", 'w') as file:
        file.write(rendered_config)

    return config

def main():
    pass

if __name__ == '__main__':
    main()