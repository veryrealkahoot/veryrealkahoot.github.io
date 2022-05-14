# read in a text file at the folder above this one/client/html

def sendwebsite(server, client, site, hassafariusers):
    html = site
    if hassafariusers:
        html = site.replace("""background-image: linear-gradient(rgba(255,255,255,0.25), rgba(255,255,255,0.25)), url("assets/background.jpg");""", """background-image: linear-gradient(rgba(255,255,255,0.25), rgba(255,255,255,0.25)), url("assets/background-android.jpg");""")
    server.send_message(client, 'updatePage' + '^' + html.split('^')[1] + '^' + html.split('^')[0] + '^' + html.split('^')[2])

entercode = ""
with open('client/html/entercode.html', 'r') as f:
    entercode = f.read()

invalidcode = ""
with open('client/html/entercodewrong.html', 'r') as f:
    invalidcode = f.read()

entername = ""
with open('client/html/joingame.html', 'r') as f:
    entername = f.read()
    
lobby = ""
with open('client/html/lobby.html', 'r') as f:
    lobby = f.read()

question = ""
with open('client/html/question.html', 'r') as f:
    question = f.read()

ownerlobby = ""
with open('client/html/owner-lobby.html', 'r') as f:
    ownerlobby = f.read()

ownerquestion = ""
with open('client/html/owner-question.html', 'r') as f:
    ownerquestion = f.read()