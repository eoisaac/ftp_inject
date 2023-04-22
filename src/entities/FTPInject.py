import argparse
import ftplib
from threading import Thread
from termcolor import colored
from src.entities.FTPClient import FTPClient


class FTPInject:
    def __init__(self, host: str = '', credentials_path: str = ''):
        self.host: str = host
        self.credentials_path: str = credentials_path
        self._FTPClient: FTPClient = None

        if not self.credentials_path:
            self._get_args()

        self.run()


    def _read_txt_file(self, file_path: str):
        with open(file_path) as lines:
            for l in lines:
                yield l.strip()


    def _run_command(self):
        print(colored('Choose an option:', 'yellow'))
        print(colored('1. Inject content', 'yellow'))
        print(colored('2. Read file', 'yellow'))
        print(colored('3. List server files', 'yellow'))
        print(colored('4. Server cmd', 'yellow'))
        print(colored('9. Exit', 'yellow'))

        option = input('> ')
        if option == '1':
            pass

        elif option == '2':
            pass

        elif option == '3':
            self._FTPClient.ls_tree()

        elif option == '4':
            self._FTPClient.cmd()

        elif option == '9':
            self.close()

        else:
            print(colored('Invalid option', 'red'))


    def _get_args(self):
        parser = argparse.ArgumentParser(description='FTPInject')
        parser.add_argument('-H', '--host', dest='host', type=str, help='Target host', required=True)
        parser.add_argument('-c', '--credentials', dest='credentials_path', type=str, help='Credentials file path', required=True)
        args = parser.parse_args()

        self.host = args.host
        self.credentials_path = args.credentials_path


    def _ftp_connect(self, user: str, pwd: str):
        try:
            ftp = FTPClient(self.host, user, pwd)
            is_connected = ftp.connect()
            if is_connected:
                self._FTPClient = ftp
        except Exception as e:
            pass


    def close(self):
        print(colored('\nDisconnecting...', 'cyan'))
        self._FTPClient.disconnect()
        exit(0)


    def run(self):
        print(colored('Connecting to ftp server...', 'yellow'))
        try:
            threads = []
            for credential in self._read_txt_file(self.credentials_path):
                user, pwd = credential.split(':')
                thread = Thread(target=self._ftp_connect, args=(user, pwd))
                thread.start()
                threads.append(thread)
            [t.join() for t in threads]

            while True:
                self._run_command()
        except KeyboardInterrupt:
            self.close()
