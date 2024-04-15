import re
import yaml

from .files import get_project_root


def is_successful(output):

    ok_match = re.compile('ok\=\d*')
    num_match = re.compile('\d+')
    ok_str = ok_match.search(output).group(0)
    ok_number = num_match.search(ok_str).group(0)
    
    failed_match = re.compile('failed\=\d*')
    failed_str = failed_match.search(output).group(0)
    failed_number = num_match.search(failed_str).group(0)
    
    if ok_number > 0 and failed_number == 0:
        return 1
    
    return 0

def idempotence(output):

    ok_match = re.compile('ok\=\d*')
    num_match = re.compile('\d+')
    ok_str = ok_match.search(output).group(0)
    ok_number = num_match.search(ok_str).group(0)
    
    failed_match = re.compile('failed\=\d*')
    failed_str = failed_match.search(output).group(0)
    failed_number = num_match.search(failed_str).group(0)
    
    changed_match = re.compile('changed\=\d*')
    changed_str = changed_match.search(output).group(0)
    changed_number = num_match.search(changed_str).group(0)
    
    if ok_number > 0 and failed_number == 0 and changed_number == 0:
        return 1
    
    return 0

def changed_report(output):

    ok_match = re.compile('ok\=\d*')
    num_match = re.compile('\d+')
    ok_str = ok_match.search(output).group(0)
    ok_number = num_match.search(ok_str).group(0)
    
    failed_match = re.compile('failed\=\d*')
    failed_str = failed_match.search(output).group(0)
    failed_number = num_match.search(failed_str).group(0)
    
    changed_match = re.compile('changed\=\d*')
    changed_str = changed_match.search(output).group(0)
    changed_number = num_match.search(changed_str).group(0)
    
    if ok_number > 0 and failed_number == 0 and changed_number > 0:
        return 1
    
    return 0

def write_playbook_on_temp_file(sample: dict):
    playbook_path = f'{get_project_root()}/data/temp/modified_playbook.yaml'
    # breakpoint()
    try:
        code = yaml.safe_load(sample['code'])
        with open(playbook_path, 'w') as file:
            yaml.dump(code, file, sort_keys=False)
            
        with open(playbook_path, 'r') as file:
            content = yaml.safe_load(file)
    except Exception as e:
        return '', -1        
    return playbook_path, content

def write_yaml_content_on_temp_file(content):
    playbook_path = f'{get_project_root()}/data/temp/modified_playbook.yaml'
    with open(playbook_path, 'w') as file:
        yaml.dump(content, file, sort_keys=False)
        
        
def restore_inv(cfg):
    inv = """[ubuntu]\nubuntu1\n\n[alpine]\nalpine1\n\n[centos]\ncentos1\n\n[redhat]\nredhat1"""
    with open(cfg['inventory_file'], 'w') as file:    
        file.write(inv)
        
        
def ubuntu_inv(cfg):
    inv = """[ubuntu]\nubuntu1"""
    with open(cfg['inventory_file'], 'w') as file:    
        file.write(inv)
        
def centos_inv(cfg):
    inv = """[centos]\ncentos1"""
    with open(cfg['inventory_file'], 'w') as file:    
        file.write(inv)
        
        
def alpine_inv(cfg):
    inv = """[alpine]\nalpine1"""
    with open(cfg['inventory_file'], 'w') as file:    
        file.write(inv)
        
        
def redhat_inv(cfg):
    inv = """[redhat]\nredhat1"""
    with open(cfg['inventory_file'], 'w') as file:    
        file.write(inv)
        
        