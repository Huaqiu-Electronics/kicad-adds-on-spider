from datetime import datetime as dt
import os

class GitWorker:
    def __init__(self, home_dir):
        self._home_dir = home_dir
        self.messages= []

    def current_time_str(self):
        return dt.now().strftime("%Y-%m-%d_%H-%M-%S")

    def add_mgs(self, msg):
        self.messages.append(msg)

    def clone_git(self):
        if not os.path.exists(self._home_dir):
            os.system(f"git clone git@gitee.com:kicad-mirror/kicad-addons.git {self._home_dir}")
            os.system("git config --global user.email 'liangtie.qian@gmail.com'")
            os.system("git config --global user.name 'liangtie.qian'")

    def pull_git(self):
        os.chdir(self._home_dir)
        os.system("git pull")

    def commit(self):
        # Join the messages
        msg = "\n".join(self.messages)
        # Clear the messages
        self.messages = []
        # cd home dir
        os.chdir(self._home_dir)
        # run git add . and git commit -m "msg"
        os.system("git add .")
        os.system(f'git commit -m "{msg}"')
        os.system("git push")



