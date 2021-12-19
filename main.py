#!/usr/bin/env python3

from bitwarden import Bitwarden
from dialogue import Dialogue

def main():
    dialogue = Dialogue()
    bitwarden = Bitwarden(dialogue)
    bitwarden.process_request()


if __name__ == '__main__':
    main()
