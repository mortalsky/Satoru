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

  f_ = open("data/commands.txt", "r")
  f = f_.read()
  f_.close()
  f = f.split("\n")
  commands = {}
  for a in f:
    a = a.split(" = ")
    if len(a) > 1:
      name = a[0]
      help = a[1]
      commands[name] = {"help": help, "name": name}
  return render_template("commands.html", commands = commands)

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
