from paths import project_path
import yaml


def test_yaml():
    with open(project_path / 'data' / 'file_configs.yaml', 'r') as yaml_file:
        obj = yaml.load(yaml_file.read(), Loader=yaml.FullLoader)
        pass
