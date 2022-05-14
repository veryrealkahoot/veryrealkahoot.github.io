from http import client
from soupsieve import select
import player
from websites import sendwebsite
import websites
from threading import Thread
from question import Question
import time

class Lobby:
    def __init__(self, code, owner, server):
        self.code = code
        self.owner = owner
        self.players = {}
        self.questions = []
        self.server = server

        self.inGame = False
        self.questionIndex = 0
        self.answeredPlayers = 0
        self.timeUntilQuestionOver = 0
        self.percision = 100
        self.questionDuration = 20 # in seconds

        self.hasNonAppleUsers = False

        self.questions = [
            Question("What is the capital of France?", 0, ["Paris", "Lyon", "Marseille", "Toulouse"]),
            Question("What is the capital of Germany?", 0, ["Berlin", "Munich", "Hamburg", "Frankfurt"]),
            Question("What is the capital of Italy?", 0, ["Rome", "Milan", "Naples", "Turin"]),
            Question("What is the capital of Spain?", 0, ["Madrid", "Barcelona", "Valencia", "Seville"]),
            Question("What is the capital of the United Kingdom?", 0, ["London", "Birmingham", "Manchester", "Liverpool"]),
            Question("What is the capital of the United States?", 0, ["Washington", "New York", "Los Angeles", "Chicago"]),
            Question("What is the capital of Brazil?", 0, ["Brasilia", "Rio de Janeiro", "Sao Paulo", "Salvador"]),
            Question("What is the capital of Canada?", 0, ["Ottawa", "Toronto", "Montreal", "Vancouver"]),
            Question("What is the capital of Australia?", 0, ["Canberra", "Sydney", "Melbourne", "Brisbane"]),
            Question("What is the capital of Japan?", 0, ["Tokyo", "Osaka", "Kyoto", "Nagoya"]),
            Question("What is the capital of China?", 0, ["Beijing", "Shanghai", "Hong Kong", "Guangzhou"]),
            Question("What is the capital of Russia?", 0, ["Moscow", "Saint Petersburg", "Novosibirsk", "Kazan"]),
        ]

    def removePlayer(self, client):
        del self.players[client['id']]
        self.refreshPlayerList()

    def parseCommand(self, client, command):
        data = command.split('|')
        if data[1] == 'createplayer':
            isOnWeb = False
            isOnSafari = False
            if data[3] == 'True':
                isOnWeb = True
            if data[4] == 'True' or data[4] == 'true':
                isOnSafari = True
            self.players[client['id']] = player.Player(client, data[2], 0, isOnWeb, isOnSafari)
            if not self.inGame:
                self.refreshPlayerList()
        print(data)
        if data[1] == 'startgame':
            if client['id'] == self.owner['id']:
                inGame = True
                print("starting...")
                thread = Thread(target=self.startGame, args = (self, ))
                thread.start()
                self.startGame()
        if data[1] == 'answer':
            currentPlayer = self.players[client['id']]
            guessedIndex = int(data[2])
            self.answeredPlayers += 1
            if self.questions[self.questionIndex].answer == guessedIndex:
                currentPlayer.score += (self.timeUntilQuestionOver / (20 * self.percision)) * 1000
            pass

    def refreshPlayerList(self):
        playerListString = ""
        self.hasNonAppleUsers = False
        for clientId in self.players:
            temp = ""
            if not self.players[clientId].isOnSafari:
                temp += """<div>""" + self.players[clientId].name + """<i class="material-icons" style="font-size:15px; color:red;">&#xe000;</i></div>"""
            else:
                temp += """<div>""" + self.players[clientId].name + """</div>"""
            if not self.players[clientId].isOnSafari:
                self.hasNonAppleUsers = True
            playerListString += temp
        html = websites.lobby.replace("<!--PLAYERLIST-->", playerListString)
        ownerhtml = websites.ownerlobby.replace("<!--PLAYERLIST-->", playerListString)
        ownerhtml = ownerhtml.replace("<--GAMEPIN GOES HERE-->", str(self.code))
        print(ownerhtml)
        sendwebsite(self.server, self.owner, ownerhtml, self.hasNonAppleUsers)
        for clientId in self.players:
            sendwebsite(self.server, self.players[clientId].client, html, self.hasNonAppleUsers)

    def startGame(self):
        print("swapped threads")
        for question in self.questions:
            print("sending question")
            self.loadQuestion(question)
            self.questionIndex += 1
        pass

    def loadQuestion(self, question):
        self.answeredPlayers = 0
        self.timeUntilQuestionOver = 20 * self.percision
        ownerHTML = websites.ownerquestion.replace("<!--QUESTION-->", question.question)
        ownerHTML = ownerHTML.replace("<!--OPTION1-->", question.options[0])
        ownerHTML = ownerHTML.replace("<!--OPTION2-->", question.options[1])
        ownerHTML = ownerHTML.replace("<!--OPTION3-->", question.options[2])
        ownerHTML = ownerHTML.replace("<!--OPTION4-->", question.options[3])
        sendwebsite(self.server, self.owner, ownerHTML, self.hasNonAppleUsers)
        for clientId in self.players:
            html = websites.question
            sendwebsite(self.server, self.players[clientId].client, html, self.hasNonAppleUsers)
        time.sleep(5)
        for x in range(20 * self.percision):
            time.sleep(1 / self.percision)
            self.timeUntilQuestionOver -= 1
            if self.answeredPlayers == len(self.players):
                break
        # print the scores of all players to the console
        for clientId in self.players:
            print(self.players[clientId].name + ": " + str(self.players[clientId].score))
        # send everyone the podium screen :)
        return
