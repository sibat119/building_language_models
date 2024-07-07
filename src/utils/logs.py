import json
import logging
from . import files

def get_log_files(config):
    files.create_path(files.get_project_root() + "/logs")
    handler = logging.StreamHandler()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    log_file = config["log_file"]
    if log_file:
        filehandler = logging.FileHandler(log_file)
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        
    return logger, handler

def record_case(success, tag="", **args):
    if success:
        files.create_path(files.get_project_root() + "/logs")
        if tag == "run":
            f = open(files.get_project_root() + "/logs/ansible_run.jsonl", "a")
        elif tag == "docker":
            f = open(files.get_project_root() + "/logs/docker.jsonl", "a")
        else:
            f = open(files.get_project_root() + "/logs/log_success.jsonl", "a")
    else:
        f = open(files.get_project_root() + "/logs/log_fail.jsonl", "a")
    log = args
    f.write(json.dumps(log) + "\n")
    f.close()
    

def log_rows(file_path, data: list):
    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        list_string = ", ".join(data)
        f.write(list_string + '\n')
