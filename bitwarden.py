from command import Command
from dialogue import Dialogue


class Bitwarden:

    session_key = ''
    folders = []

    def __init__(self, dialogue: Dialogue, command: Command):
        self.command = command
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

        template = self.command.get_item_template(self.session_key)
        template['type'] = 2
        template['name'] = name
        template['notes'] = note
        template['folderId'] = self.folders[selected_folder_index - 1]['id']

        secure_note_template = self.command.get_secure_note_template(self.session_key)
        secure_note_template['type'] = 0
        template['secureNote'] = secure_note_template

        status = self.command.save_item(self.session_key, template)
        self.dialogue.print_status(status)
        exit(status)


    def create_new_login(self):
        name = input('Enter a name for the new login: ')
        username = input('Enter a username for the new login: ')
        password = self.dialogue.get_new_password()
        uri = input('Enter a url for the new login if it applies: ')
        selected_folder_index = self.dialogue.select_folder(self.folders)
        if self.dialogue.confirm_choice(f"Are you sure you want to create a login named {name}, username {username}, password {password}?") != 'y':
            print('User aborted.')
            exit(1)

        template = self.command.get_item_template(self.session_key)
        login_template = self.command.get_login_template(self.session_key)

        if uri != '':
            uri_template = self.command.get_uri_template(self.session_key)
            uri_template['uri'] = uri
            login_template['uris'].append(uri_template)


        template['name'] = name
        template['folderId'] = self.folders[selected_folder_index - 1]['id']
        login_template['username'] = username
        login_template['password'] = password
        login_template['totp'] = ''
        template['login'] = login_template

        status = self.command.save_item(self.session_key, template)
        self.dialogue.print_status(status)
        exit(status)


    def process_new_folder_request(self):
        option = input('Enter the name of the new folder: ')
        if self.dialogue.confirm_choice(f"Are you sure you want to create a folder named {option}?") != 'y':
            print('User aborted.')
            exit(1)

        template = self.command.get_folder_template(self.session_key)
        template['name'] = option

        status = self.command.save_folder(self.session_key, template)
        self.dialogue.print_status(status)
        exit(status)


    def get_folders(self):
        self.folders = self.command.list_folders(self.session_key)


    def check_bitwarden_install(self):
        status = self.command.check_bw_install()
        if status != 0:
            print('Bitwarden CLI is not installed. Please install it first and try again.')
            exit(1)


    def check_bitwarden_login(self):
        status_json = self.command.check_login()
        if status_json['status'] == 'unauthenticated':
            print('You are not logged into Bitwarden. Please use the "bw login" command to log in and try again.')
            exit(1)


    def unlock_vault(self):
        password = self.dialogue.get_users_password()
        self.session_key = self.command.get_session_key(password)


    def sync_vault(self):
        status = self.command.sync_vault(self.session_key)
        if status != 0:
            print('Unable to sync the vault. Please try again later.')
            exit(1)
