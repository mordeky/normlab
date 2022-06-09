import yaml
from paths import yaml_config_file

# reject_folders = ['.idea']
# reject_file_types = ['.class', '.exe', '.obj', '.DS_Store', '.git']
# vip_file_types = ['.doc', '.docx', '.pdf']


with open(yaml_config_file, 'r', encoding='UTF-8') as yaml_file:
    obj = yaml.load(yaml_file.read(), Loader=yaml.FullLoader)
    reject_folders = obj['reject_folders'].rstrip(',').split(', ')
    reject_subpaths = obj['reject_subpaths'].rstrip(',').split(', ')
    reject_structured_folders = obj['reject_structured_folders'].rstrip(',').split(', ')
    reject_structured_folders = [m.split('||') for m in reject_structured_folders]
    reject_file_types = obj['reject_file_types'].rstrip(',').split(', ')
    reject_files = obj['reject_files'].rstrip(',').split(', ')
    vip_file_types = obj['vip_file_types'].rstrip(',').split(', ')
    pass
