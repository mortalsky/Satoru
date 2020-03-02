from threading import Thread
from flask import Flask, render_template, redirect, jsonify
import json

app = Flask('')

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/stats')
def stats():

  with open("data/stats.json", "r") as f:

    l = json.load(f)
    
  return render_template("stats.html", library = l["library"], python = l["python"], memory = l["memory"], cpu = l["cpu"], running = l["running"], guilds = l["guilds"], users = l["users"], uptime = l["uptime"])

@app.route("/api/stats")
def api_stats():

  with open("data/stats.json", "r") as f:

    l = json.load(f)

  return jsonify(l)

@app.route('/commands')
def commands():

  with open("data/commands.json", "r") as f:

    l = json.load(f)

  res = ""

  for a in l:

    res += f"""<a class = 'commandname'>e?{a}</a><br><a class = 'commandhelp'>&nbsp;{l[a]}</a></li><br><br>\n"""

  html0 = '''<!DOCTYPE html>
<head>
  <!-- Meta Tags -->

  <title>Satoru - Discord Bot</title> 
  <meta name="viewport" content="width=device-width">
  <meta name="description" content="A multifunction Discord Bot with Moderation and Fun!">
  <meta name="keywords" content="HTML,CSS,XML,JavaScript">
  <meta name="author" content="Sebastiano Girotto">
  <meta property = "og:title" content = "Satoru - Discord Bot">
  <meta property = "og:description" content = "A multifunction Discord Bot with Moderation and Fun!">
  <meta property = "og:image" content = "https://i.seba.gq/satoru.png">
  <meta name="theme-color" content="#fffad9">

  <!-- Links -->

  <link href="https://fonts.googleapis.com/css?family=Lato&display=swap" rel="stylesheet">
  <link rel="icon" href="https://i.seba.gq/satoru.png"/>

  <!-- Style -->

  <style>
    body {
        font-family: 'Lato', sans-serif;
        margin-top: 5%;
    }

    .link {
        color: blue;
        text-decoration: none;
        transition-duration: .2s;
    }

    .link:hover {
        background: #dcdde1;
        transform: rotate(10deg);
    }

    h1 {
        transition-duration: 1s;
        text-align: center;
    }

    h1:hover {
        transform: rotate(10deg);
    }

    .commandhelp {
        border-left-color: gray;
        border-left-style: solid;
    }

    .commands {
      margin-left: 30%;
      margin-right: 10%;
    }
  </style> 
</head>
<body>
  <h1>Satoru Commands</h1>'''

  html1 = f'''
  <div class = "commands">
  \n<ul>{res}</ul>
  </div>
'''

  html2 = '''<script>
    if (window.location.protocol === "http:") {
      location.href = "https://satoru.seba.gq/"
    }
  </script>
</body>'''

  with open("templates/commands.html", "w") as f:

    f.write(" ")
    f.write(html0)
    f.write(html1)
    f.write(html2)
    
  return render_template("commands.html")

@app.route("/invite")
def invite():

  return redirect("https://discordapp.com/api/oauth2/authorize?client_id=635044836830871562&permissions=321606&scope=bot")

@app.route("/github")
def github():
  return redirect("https://github.com/ssebastianoo/satoru")

@app.errorhandler(404)
def not_found(error):
  return redirect("/")

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()
