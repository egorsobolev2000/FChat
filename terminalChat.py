import getpass
from termcolor import colored
from dotenv import load_dotenv
load_dotenv(dotenv_path = '.evn')

class terminalChat():
    pusher = None
    channel = None
    cahtroom = None
    clienr_pusher = None
    user = None
    users = {
    "egor": "egor'spassword"
    "sam": "sam'spassword"
    }
    chatrooms = ['it', 'summer']

    #Точка входа в чат
    def main(self):
        self.login()
        self.selectChatroom()
        while True:
            self.getInput()
    #Валидация даных для входа в систему
    def login(self):
        username = input("Please enter your name: ")
        password = getpass.getpass("Please enter %s's Password: " % username)
        if username in self.users:
            if self.users[username] == password:
                self.user = username
            else:
                 print(colored("Your password is incorrect", "red"))
                self.login()
    #Выбор чата из предоставленного списка
    def slelctChatroom(self):
        print("Available chatrooms are %s" %str(self.chatrooms))
        chatroom = input(colored("Select a chatroom: ", "green"))
        if chatroom in self.chatrooms:
            self.chatroom = chatroom
            self.initPusher()
        else:
            print(colored("No such chatroom in our list", "red"))
            self.selectChatroom()
    def getInput(self):
        message = input(colored("{}: " .format(self.user), "green")

if __name__ == "__main__":
    terminalChat().main()
