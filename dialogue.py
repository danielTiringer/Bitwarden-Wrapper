class Dialogue:
    main_menu_options = {
        1: 'Create new item',
        2: 'Create new folder',
        3: 'Cancel',
    }
    item_types = {
        1: 'Login',
        2: 'Secure Note',
        3: 'Card',
        4: 'Identity',
        5: 'Cancel',
    }

    def prompt_main_menu(self):
        return self.prompt_option_selection(self.main_menu_options)

    def prompt_item_type_selection(self):
        return self.prompt_option_selection(self.item_types)

    def prompt_option_selection(self, options):
        print('Please select what you want to do:')
        self.print_menu(options)
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number...')

        return option

    def confirm_choice(self, choice_string):
        print(choice_string)
        while True:
            confirm = input('[y]Yes or [n]No: ')
            if confirm in ('y', 'n'):
                return confirm
            else:
                print('Invalid Option. Please Enter a Valid Option.')

    def print_menu(self, list):
        for key in list.keys():
            print(key, '--', list[key])
