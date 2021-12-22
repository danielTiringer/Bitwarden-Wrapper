import json
import re
import subprocess
from dialogue import Dialogue


class Bitwarden:
    session_key = ''
    folders = []

    def __init__(self, dialogue: Dialogue):
        self.dialogue = dialogue
        self.check_bitwarden_install()
        self.check_bitwarden_login()
        self.unlock_vault()
        self.sync_vault()
        self.get_folders()


    def process_request(self):
        while(True):
            option = self.dialogue.prompt_main_menu()

            if option == 1:
                self.process_new_item_request()

            if option == 2:
                self.process_new_folder_request()

            if option == 3:
                print('User aborted.')
                exit(0)


    def process_new_item_request(self):
        while(True):
            option = self.dialogue.prompt_item_type_selection()
            if option == 1:
                self.create_new_login()
            if option == 2:
                self.create_new_secure_note()
            if option == 5:
                print('User aborted.')
                exit(0)


    def create_new_secure_note(self):
        name = input('Enter a name for the new secure note: ')
        note = input('Enter the note you wish to save: ')
        selected_folder_index = self.dialogue.select_folder(self.folders)
        if self.dialogue.confirm_choice(f"Are you sure you want to create a secure note named {name} containing {note}?") != 'y':
            print('User aborted.')
            exit(1)

        template = json.loads(subprocess.getoutput(f"bw get template item --session {self.session_key}"))
        template['type'] = 2
        template['name'] = name
        template['notes'] = note
        template['folderId'] = self.folders[selected_folder_index - 1]['id']

        secure_note_template = json.loads(subprocess.getoutput(f"bw get template item.secureNote --session {self.session_key}"))
        secure_note_template['type'] = 0
        template['secureNote'] = secure_note_template

        updated_template_json = json.dumps(template, separators = (',', ':'))
        output = subprocess.getstatusoutput(f"echo '{updated_template_json}' | bw encode | bw create item --session {self.session_key}")
        
        if output[0] == 0:
            print("The note was created.")
        else:
            print("There was a problem creating the note.")

        exit(output[0])


    def create_new_login(self):
        name = input('Enter a name for the new login: ')
        username = input('Enter a username for the new login: ')
        password = self.dialogue.get_new_password()
        uri = input('Enter a url for the new login if it applies: ')
        selected_folder_index = self.dialogue.select_folder(self.folders)
        if self.dialogue.confirm_choice(f"Are you sure you want to create a login named {name}, username {username}, password {password}?") != 'y':
            print('User aborted.')
            exit(1)

        template = json.loads(subprocess.getoutput(f"bw get template item --session {self.session_key}"))
        print(json.dumps(template, indent = 4))
        login_template = json.loads(subprocess.getoutput(f"bw get template item.login --session {self.session_key}"))
        template['name'] = name
        template['folderId'] = self.folders[selected_folder_index - 1]['id']
        login_template['username'] = username
        login_template['password'] = password
        login_template['totp'] = ''

        if uri != '':
            uri_template = json.loads(subprocess.getoutput(f"bw get template item.login.uri --session {self.session_key}"))
            uri_template['uri'] = uri
            login_template['uris'].append(uri_template)

        template['login'] = login_template
        updated_template_json = json.dumps(template, separators = (',', ':'))
        output = subprocess.getstatusoutput(f"echo '{updated_template_json}' | bw encode | bw create item --session {self.session_key}")
        
        if output[0] == 0:
            print("The login was created.")
        else:
            print("There was a problem creating the login.")

        exit(output[0])


    def process_new_folder_request(self):
        option = input('Enter the name of the new folder: ')
        if self.dialogue.confirm_choice(f"Are you sure you want to create a folder named {option}?") != 'y':
            print('User aborted.')
            exit(1)

        template_json = subprocess.getoutput(f"bw get template folder --session {self.session_key}")
        template = json.loads(template_json)
        template['name'] = option
        updated_template_json = json.dumps(template, separators=(',', ':'))
        output = subprocess.getstatusoutput(f"echo '{updated_template_json}' | bw encode | bw create folder --session {self.session_key}")

        if output[0] == 0:
            print("The folder was created.")
        else:
            print("There was a problem creating the folder.")

        exit(output[0])


    def get_folders(self):
        folders_string = subprocess.getoutput(f"bw list folders --session {self.session_key}")
        self.folders = json.loads(folders_string)


    def check_bitwarden_install(self):
        status = subprocess.getstatusoutput('command -v bw')
        if status[0] != 0:
            print('Bitwarden CLI is not installed. Please install it first and try again.')
            exit(1)


    def check_bitwarden_login(self):
        status_string = subprocess.getoutput('bw status')
        status_json = json.loads(status_string)
        if status_json['status'] == 'unauthenticated':
            print('You are not logged into Bitwarden. Please use the "bw login" command to log in and try again.')
            exit(1)


    def unlock_vault(self):
        password = self.dialogue.get_users_password()
        status = subprocess.getoutput(f"echo {password} | bw unlock")
        substring = re.search(r'"([A-Za-z0-9/+=]*)=="', status)
        self.session_key = substring.group()


    def sync_vault(self):
        status = subprocess.getstatusoutput(f"bw sync --session {self.session_key}")
        if status[0] != 0:
            print('Unable to sync the vault. Please try again later.')
            exit(1)
