import subprocess
from src.cfg_reader import primary
def run_ansible_playbook(playbook_path):
        """Helper method to run shell commands and return output."""
        config = primary.load('conf/config.yaml')
        inventory = config["inventory_file"]
        private_key = config["private_key"]
        become_password_file = config["become_password_file"]
        ansible_command = [
                "ansible-playbook", playbook_path, 
                "-i", inventory, 
                "--private-key", private_key,
                "--become-password-file", become_password_file,
                "-vvv"
        ]
    
        output = subprocess.run(
                ansible_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=300,
                text=True
        )
    
        return output

def get_yaml_file(path):
        # TODO: finish this
        return ""