#!/usr/bin/env python3

from bitwarden import Bitwarden
from command import Command
from dialogue import Dialogue

def main():
    command = Command()
    dialogue = Dialogue()
    bitwarden = Bitwarden(dialogue, command)
    bitwarden.process_request()


if __name__ == '__main__':
    main()
