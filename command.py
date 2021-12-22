import json
import re
import subprocess


class Command:

    def check_bw_install(self):
        status = subprocess.getstatusoutput('command -v bw')
        return status[0]


    def check_login(self):
        status_string = subprocess.getoutput('bw status')
        return json.loads(status_string)


    def get_folder_template(self, session_key):
        template_string = subprocess.getoutput(f"bw get template folder --session {session_key}")
        return json.loads(template_string)


    def get_item_template(self, session_key):
        template_string = subprocess.getoutput(f"bw get template item --session {session_key}")
        return json.loads(template_string)


    def get_login_template(self, session_key):
        template_string = subprocess.getoutput(f"bw get template item.login --session {session_key}")
        return json.loads(template_string)


    def get_secure_note_template(self, session_key):
        template_string = subprocess.getoutput(f"bw get template item.secureNote --session {session_key}")
        return json.loads(template_string)


    def get_session_key(self, password):
        status = subprocess.getoutput(f"echo {password} | bw unlock")
        substring = re.search(r'"([A-Za-z0-9/+=]*)=="', status)
        return substring.group()


    def get_uri_template(self, session_key):
        template_string = subprocess.getoutput(f"bw get template item.login.uri --session {session_key}")
        return json.loads(template_string)


    def list_folders(self, session_key):
        folders_string = subprocess.getoutput(f"bw list folders --session {session_key}")
        return json.loads(folders_string)


    def save_item(self, session_key, template):
        updated_template_json = json.dumps(template, separators = (',', ':'))
        status = subprocess.getstatusoutput(f"echo '{updated_template_json}' | bw encode | bw create item --session {session_key}")
        return status[0]


    def save_folder(self, session_key, template):
        updated_template_json = json.dumps(template, separators=(',', ':'))
        status = subprocess.getstatusoutput(f"echo '{updated_template_json}' | bw encode | bw create folder --session {session_key}")
        return status[0]


    def sync_vault(self, session_key):
        status = subprocess.getstatusoutput(f"bw sync --force --session {session_key}")
        return status[0]
