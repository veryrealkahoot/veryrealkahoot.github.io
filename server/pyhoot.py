from websocket_server import WebsocketServer
import logging
import random

from websites import sendwebsite
import websites
import lobby

lobbies = {}
clientToCode = {}

def new_client(client, server):
    sendwebsite(server, client, websites.entercode, False)

def message_received(client, server, message):
    data = message.split('|')
    if data[0] == 'createlobby':
        code = str(random.randint(100000, 999999))
        print(code)
        lobbies[code] = lobby.Lobby(code, client, server)
        clientToCode[client['id']] = code
        html = websites.ownerlobby.replace('<--GAMEPIN GOES HERE-->', str(code))
        sendwebsite(server, client, html, False)
    elif data[0] == 'checkgamevalid':
        if data[1] in lobbies:
            sendwebsite(server, client, websites.entername, False)
        else:
            sendwebsite(server, client, websites.invalidcode, False)
    else:
        if client['id'] not in clientToCode:
            clientToCode[client['id']] = data[0]
        lobbies[data[0]].parseCommand(client, message)

def remove_client(client, server):
    code = clientToCode[client['id']]
    if lobbies[code].owner['id'] == client['id']:
        for player in lobbies[code].players:
            sendwebsite(server, lobbies[code].players[player].client, websites.entercode, False)
            del clientToCode[lobbies[code].players[player].client['id']]
        del lobbies[code]
    else:
        lobbies[code].removePlayer(client)
    del clientToCode[client['id']]

server = WebsocketServer(host='0.0.0.0', port=11000, loglevel=logging.INFO, key="key.pem", cert="cert.pem")
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.set_fn_client_left(remove_client)

server.run_forever()