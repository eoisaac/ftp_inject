import os
import ftplib
from termcolor import colored

class FTPClient:
    def __init__(self, host: str = '', user: str = '', pwd: str = ''):
        self._client: ftplib.FTP = None
        self.host: str = host
        self.user: str = user
        self.pwd: str = pwd
        self.current_dir: str = '/'
        self.commands = {
            'ls': self._ls,
            'ls_tree': self.ls_tree,
            'mkdir': self._mkdir,
            'touch': self._touch,
            'mv': self._mv,
            'cd': self._cd,
            'cat': self._cat,
            'pwd': self._pwd,
            'nano': self._nano,
            'exit': self._exit,
            'help': self._help,
        }

    def connect(self):
        print(colored(f'Trying {self.user}:{self.pwd}', 'yellow'))

        try:
            ftp = ftplib.FTP(self.host, timeout=5)
            response = ftp.login(self.user, self.pwd)
            if all(x in response.lower() for x in ['230', 'login successful.']):
                print(colored(f'[*] {self.host} FTP Login Success: {self.user}:{self.pwd}', 'green'))
                self._client = ftp
                return True

            return False
        except Exception as e:
            pass


    def disconnect(self):
        if self._client:
            self._client.quit()


    def cmd(self):
        print(colored(f'Welcome to FTP shell. Host: {self.host}', 'green'))
        print(colored("Type 'help' to see available commands.", 'green'))

        while True:
            try:
                command = input(colored(f'ftp:{self.current_dir} $ ', 'blue'))
                command_parts = command.split(' ')
                command_name = command_parts[0]

                if command_name in self.commands:
                    command_fn = self.commands[command_name]
                    args = command_parts[1:]
                    result = command_fn(*args)
                    if result:
                        print(result)

                else:
                    print(colored(f'Invalid command: {command_name}', 'red'))

            except Exception as e:
                pass
            except KeyboardInterrupt:
                self._exit()


    def _mkdir(self, dir_name):
        if self._client:
            self._client.mkd(f'{self.current_dir}/{dir_name}')
            return f"Directory '{dir_name}' created successfully."


    def _touch(self, file_name):
        if self._client:
            self._client.cwd(self.current_dir)
            self._client.storbinary(f"STOR {file_name}", open(file_name, 'rb'))
            return f"File '{file_name}' created successfully."


    def _mv(self, old_path, new_path):
        if self._client:
            self._client.rename(old_path, new_path)
            return f'{old_path} renamed to {new_path} successfully.'


    def _cd(self, dir_name):
        if self._client:
            self._client.cwd(os.path.join(self.current_dir, dir_name))
            self.current_dir = self._client.pwd()
            return f'Directory changed to {self.current_dir}'


    def _cat(self, file_name):
        if self._client:
            try:
                with self._client.open(file_name) as f:
                    return f.read()
            except Exception as e:
                return f'Error: {str(e)}'


    def _nano(self, file_name):
        if self._client:
            local_file_path = os.path.join(os.getcwd(), file_name)
            self._client.retrbinary(f'RETR {file_name}', open(local_file_path, 'wb').write)
            os.system(f'nano {local_file_path}')
            self._client.storbinary(f'STOR {file_name}', open(local_file_path, 'rb'))
            os.remove(local_file_path)
            return f"File '{file_name}' edited successfully."


    def _ls(self, path=""):
        if self._client:
            files = self._client.nlst(path or self.current_dir)
            return '\n'.join(files)


    def ls_tree(self, path='', level=0):
        if self._client:
            files = self._client.nlst(path or self.current_dir)
            for file in files:
                if '.' in file:
                    print(f"| {'| ' * level}- {file}")
                else:
                    print(f"| {'| ' * level}+ {file}")
                    self.ls_tree(path=file, level=level+1)

    def _pwd(self):
        if self._client:
            return self.current_dir


    def _help(self):
        print(colored('Available commands:', 'green'))
        print('\n'.join(self.commands.keys()))


    def _exit(self):
        print(colored('\nGoodbye!', 'green'))
        self.disconnect()
        exit(0)
