
class Dialogue:
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
