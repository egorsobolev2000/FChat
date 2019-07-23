#!/usr/bin/python3
# -*- coding: utf-8 -*-clear
import getpass
from termcolor import colored
from pusher import Pusher
import pysher
from dotenv import load_dotenv
import os
import json

load_dotenv(dotenv_path='.env')

class terminalChat():
    pusher = None       #Содержит экземпляр сервера
    channel = None      #Содержит экземпляр Pusher канала
    chatroom = None     #Название канала
    clientPusher = None #будет содержать экземпляр клиента Pusher
    user = None         #информацию о текущем вошедшем в систему пользователе
    users = {
        "egor": "00000",
        "user": "user"
    }
    chatrooms = ['Somechat']

    #точка входа в приложение
    def main(self):
        self.login()
        self.selectChatroom()
        while True:
            self.getInput()

    #функция входа в систему
    def login(self):
        username = input("Please enter your username: ")
        password = getpass.getpass("Please enter %s's Password: " % username)
        if username in self.users:
            if self.users[username] == password:
                self.user = username
            else:
                print(colored("Your password is incorrect", "red"))
                self.login()
        else:
            print(colored("Your username is incorrect", "red"))
            self.login()

    #Выбор чата из предоставленного списка
    def selectChatroom(self):
        print(colored("Available chat's are %s" % str(self.chatrooms), "blue"))
        chatroom = input(colored("Please select a chat: ", "green"))
        if chatroom in self.chatrooms:
            self.chatroom = chatroom
            self.initPusher()
        else:
            print(colored("No such chat in our list", "red"))
            self.selectChatroom()

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

    #когда происходит новое событие
    def pusherCallback(self, message):
        message = json.loads(message)
        if message['user'] != self.user:
            print(colored("{}: {}".format(message['user'], message['message']), "blue"))
            print(colored("{}: ".format(self.user), "green"))

    # Функция для получения текущего сообщения
    def getInput(self):
        message = input(colored("{}: ".format(self.user), "green"))
        self.pusher.trigger(self.chatroom, u'newmessage', {"user": self.user, "message": message})


if __name__ == "__main__":
    terminalChat().main()
