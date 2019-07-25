#!/usr/bin/python3
# -*- coding: utf-8 -*-clear
import getpass
import pyautogui
from termcolor import colored
from pusher import Pusher
import pysher
from dotenv import load_dotenv
import os
import json
import sys
from intro import *

# NOTE: Добавить к сообщения время отправки

# Функция предварительной очистки консоли
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
cls()

load_dotenv(dotenv_path='.env')
screen_code = "\033[1A\033[2K"


class terminalChat():
    pusher = None       #Содержит экземпляр сервера
    channel = None      #Содержит экземпляр Pusher канала
    chatroom = None     #Название канала
    clientPusher = None #будет содержать экземпляр клиента Pusher
    user = None         #информацию о текущем вошедшем в систему пользователе
    users = {
        "tad": "tad",
        "sam": "sam"
    }
    chatrooms = ['Somechat', 'Another', '1']

    #точка входа в приложение
    def main(self):
        self.login()
        self.selectChatroom()
        while True:
            self.getInput()

    #функция входа в систему
    def login(self):
        # Ввод данных
        eggIntro()
        intro()
        username = input("Username: ")
        password = getpass.getpass("Enter %s's Password: " % username)
        if username in self.users:
            cls()
            if self.users[username] == password:
                self.user = username
            else:
                cls()
                print(colored("Your password is incorrect", "red"))
                self.login()
        else:
            cls()
            print(colored("Your username is incorrect", "red"))
            self.login()

    #Выбор чата из предоставленного списка
    def selectChatroom(self):
        intro()
        i = 0
        for chat in self.chatrooms:
            i += 1
            print([i], colored(chat, "blue").center(10))
        chatroom = input(colored("\nSelect a chat: ", "green"))
        if chatroom in self.chatrooms:
            cls()
            self.chatroom = chatroom
            self.initPusher()
        else:
            cls()
            print(colored("No such chat in our list", "red"))
            self.selectChatroom()
        cls()
        print("\x1b[6;30;42m","Chat [ {} ]\x1b[0m\n".format(chatroom))

    #Функция инициализации
    def initPusher(self):
        self.pusher = Pusher(app_id=os.getenv('PUSHER_APP_ID', None), key=os.getenv('PUSHER_APP_KEY', None), secret=os.getenv('PUSHER_APP_SECRET', None), cluster=os.getenv('PUSHER_APP_CLUSTER', None))
        # инициализирую новый Pysher клиент передавая APP_KEY
        self.clientPusher = pysher.Pusher(os.getenv('PUSHER_APP_KEY', None), os.getenv('PUSHER_APP_CLUSTER', None))
        # Связываюсь с соеденением событием и передаю connectHandler в качестве обратного вызова
        self.clientPusher.connection.bind('pusher:connection_established', self.connectHandler)
        self.clientPusher.connect()

    #Её вызывать когда Pusher установил соеденение
    def connectHandler(self, data):
        self.channel = self.clientPusher.subscribe(self.chatroom)
        self.channel.bind('newmessage', self.pusherCallback)

    #когда происходит новое сообщение
    def pusherCallback(self, message):
        message = json.loads(message)
        if message['user'] != self.user:
            if message['user'] != self.user:
                sys.stdout.write('\033[1A')
                print("\n\x1b[1;34m{}\x1b[0m: {}".format(message['user'], message['message']))
            print("\x1b[1;31m{}\x1b[0m: ".format(self.user))
            sys.stdout.write('\n\033[1A')
            #pyautogui.press('esc')
            if message['user'] != self.user:
                sys.stdout.write(screen_code)

    # Функция для получения текущего сообщения
    def getInput(self):
        message = input("\x1b[1;31m{}\x1b[0m: ".format(self.user))
        if message == "":
            sys.stdout.write(screen_code)
        elif message != "":
            self.pusher.trigger(self.chatroom, u'newmessage', {"user": self.user, "message": message})
        else:
            print(colored("Something went wrong", 'red'))


if __name__ == "__main__":
    terminalChat().main()
