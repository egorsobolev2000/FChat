#!/usr/bin/python3
# -*- coding: utf-8 -*-clear
import getpass
import pysher
import os
import json
from pusher import Pusher
from termcolor import colored
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class terminalChat():
    pusher = None       #Содержит экземпляр сервера
    channel = None      #Содержит экземпляр Pusher канала
    cahtroom = None     #Название канала
    clientPusher = None #будет содержать экземпляр клиента Pusher
    user = None         #информацию о текущем вошедшем в систему пользователе
    users = {
    "egor": "egor'spassword"
    "sam": "sam'spassword"
    }
    chatrooms = ['it', 'summer']

    #точка входа в приложение
    def main(self):
        self.login()
        self.selectChatroom()
        while True:
            self.getInput()

    #функция входа в систему
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

    #Функция инициализации
    def initPusher(self):
        self.pusher = Pusher(app_id = os.getenv('PUSHER_APP_ID', None),
        key = os.getenv('PUSHER_APP_KEY', None),
        secret = os.getenv('PUSHER_APP_SECRET', None),
        cluster = os.getenv('PUSHER_APP_CLUSTER', None))
        # инициализирую новый Pysher клиент передавая APP_KEY
        self.clientPusher = pysher.Pusher(os.getenv('PUSHER_APP_KEY', None), os.getenv('PUSHER_APP_CLUSTER', None))
        # Связываюсь с соеденением событием и передаю connectHandler в качестве обратного вызова
        self.clientPusher.connection.bind('pusher:connection_established', self.connectHandler) #получаю аргумент с именем data
        self.clientPusher.connect()

    #Её вызывать когда Pusher установил соеденение
    def connectHandler(self, data):
        self.channel = self.clientPusher.subscribe(self.chatroom)
        self.channel.bind('newmessage', self.pusherCallback)

    #когда происходит новое событие
    def pusherCallback(self, message):
        message = json.loads(message)
        if message['user'] != self.user:
            print(colored("{}: {}".format(message['user']), message['message']), "blue")
            print(colored("{}: ".format(self.user), "green"))

    # Функция для получения текущего сообщения
    def getInput(self):
        message = input(colored("{}: " .format(self.user), "green")
        self.pusher.trigger(self.chatroom, u'newmessage', {"user": self.user, "message": message})

if __name__ == "__main__":
    terminalChat().main()
