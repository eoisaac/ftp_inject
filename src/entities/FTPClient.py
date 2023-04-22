import os
import io
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
            'mkdir': self._mkdir,
            'touch': self._touch,
            'mv': self._mv,
            'cd': self._cd,
            'cat': self._cat,
            'pwd': self._pwd,
            'nano': self._nano,
            'rm': self._rm,
            'shutdown': self._shutdown,
            'help': self._help,
        }


    def _mkdir(self, dir_name):
        dirs = dir_name.split('/')
        current_dir = self.current_dir
        for d in dirs:
            dir = f'{current_dir}/{d}'
            self._client.mkd(dir)
            current_dir = dir
        return f"Directory '{current_dir}' created successfully."


    def _touch(self, file_name):
        self._client.cwd(self.current_dir)
        self._client.storbinary(f"STOR {file_name}", io.BytesIO())
        return f"File '{file_name}' created successfully."


    def _mv(self, old_path, new_path):
        self._client.rename(old_path, new_path)
        return f'{old_path} renamed to {new_path} successfully.'


    def _cd(self, dir_name):
        self._client.cwd(os.path.join(self.current_dir, dir_name))
        self.current_dir = self._client.pwd()
        return f'Directory changed to {self.current_dir}'


    def _cat(self, file_name):
        try:
            with io.BytesIO() as f:
                self._client.retrbinary(f'RETR {file_name}', f.write)
                f.seek(0)
                return f.read().decode()
        except Exception as e:
            return f'Error: {str(e)}'


    def _nano(self, file_name):
        local_file_path = os.path.join(os.getcwd(), file_name)
        self._client.retrbinary(f'RETR {file_name}', open(local_file_path, 'wb').write)
        os.system(f'nano {local_file_path}')
        self._client.storbinary(f'STOR {file_name}', open(local_file_path, 'rb'))
        os.remove(local_file_path)
        return f"File '{file_name}' edited successfully."


    def _ls_tree(self, path='', level=0):
        files = self._client.nlst(path or self.current_dir)
        for file in files:
            if '.' in file:
                print(f"| {'| ' * level}- {file.split('/')[-1]}")
            else:
                print(f"| {'| ' * level}+ {file.split('/')[-1]}")
                self._ls_tree(path=file, level=level+1)


    def _ls(self, path="", **kwargs):
        files = self._client.nlst(path or self.current_dir)
        if kwargs.get('-t'):
            return self._ls_tree()
        else:
            return '\n'.join([f.replace(self.current_dir, '') for f in files])


    def _rm(self, path, **kwargs):
        if kwargs.get('-r'):
            self._client.cwd(path)
            for file_name in self._client.nlst():
                if '.' in file_name:
                    self._client.delete(file_name)
                else:
                    self._rm(file_name, **kwargs)
            self._client.cwd('..')
            self._client.rmd(path)
            return f"Directory '{path}' removed"

        else:
            self._client.delete(path)
            return f"File '{path}' removed."

    def _pwd(self):
        return self.current_dir


    def _help(self):
        print(colored('Available commands:', 'green'))
        print('\n'.join(self.commands.keys()))


    def _shutdown(self):
        print(colored('\nGoodbye!', 'cyan'))
        self.disconnect()
        exit(0)


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
                flags = [arg for arg in command_parts[1:] if arg.startswith('-')]
                args = [arg for arg in command_parts[1:] if not arg.startswith('-')]

                if command_name in self.commands:
                    if self._client:
                        command_fn = self.commands[command_name]
                        result = command_fn(*args, **dict(zip(flags, [True] * len(flags))))
                        if result:
                            print(f'{result}\n')
                elif command_name == 'exit':
                    break
                else:
                    print(colored(f'Invalid command: {command_name}', 'red'))
            except Exception as e:
                pass
            except KeyboardInterrupt:
                break
 