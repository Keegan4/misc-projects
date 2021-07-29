import os
import discord
import requests

import random
from keep_alive import keep_alive
from replit import db
from discord.ext import commands

#works by responding to events

client = discord.Client()

def reddit():
  client_id = "y5TYoOG7MGecJQ"
  secret_key = os.environ['redditKey']
  auth = requests.auth.HTTPBasicAuth(client_id, secret_key)
  data = {
    "grant_type": "password",
    "username": "Theruin15",
    "password": os.environ['pw']
  }
  headers = {"User-Agent": "MYAPI/0.0.1"}
  res = requests.post("https://www.reddit.com/api/v1/access_token", auth = auth, data = data, headers = headers)
  print(res.json())
  token = res.json()["access_token"]
  headers['Authorization'] = f'bearer {token}'
  res = requests.get('https://oauth.reddit.com/r/mathmemes/hot', headers = headers, params={'limit': '100'})
  pos = []
  for post in res.json()['data']['children']:
    pos.append(post['data']["title"] + '\n' + post['data']['selftext'])
  return pos



def get_quote():
  response = requests.get("https://v2.jokeapi.dev/joke/Programming")
  data = response.json()
  if "setup" in data:
    set_up = data["setup"]
    delivery = data["delivery"]
    joke = set_up + "-" + delivery
  else:
    joke = data["joke"]
  return joke

def moments(msg):
  if "patani" in db.keys():
    value = db["patani"]
    value.append(msg)
    db["patani"] = value
  else:
    db["patani"] = [msg]

def delete(index):
  value = db["patani"]
  if index < len(value):
    del value[index]
    db["patani"] = value

def lst():
  if "patani" in db.keys():
    if len(db["patani"]) == 0:
      return "There are no moments"
    value = db["patani"]
    display = ""
    counter = 0
    for i in value:
      display = display + f"{counter} - " + i + "\n"
      counter += 1
    return display
  else:
    return "There are no moments"
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
@client.event
async def on_message(message):
  msg = message.content
  
  if message.author == client.user:
    return 
  if msg.startswith("$jokes"):
    quote = random.choice(reddit())
    await message.channel.send(quote)
  elif msg.startswith("$joke"):
    query = msg.split("$joke ", 1)[-1]
    quote = get_quote()
    if query == "tts":
      await message.channel.send(quote, tts = True)
    else:
      await message.channel.send(quote)
  elif msg.startswith("$subscribed"):
    if "subscribers" in db.keys():
      value = db["subscribers"]
      value.append(message.author())
      db["subscribers"] = value
    else:
      db["subscribers"] = message.author()
  if msg.startswith("$moment"):
    lstMoments = db["patani"]
    moment = random.choice(lstMoments)
    await message.channel.send(moment)
  if msg.startswith("$new"):
    moment = msg.split("$new ", 1)[1] #takes the second value from the message
    moments(moment)
    await message.channel.send("Successful Submission")
  if msg.startswith("$del"):
    rem = int(msg.split("$del ", 1)[1])
    delete(rem)
    await message.channel.send("Successfully Deleted \n" + lst())
  if msg.startswith("$list"):
      await message.channel.send(lst())

''''
def sending():

  daily = reddit()[:3]
  for i in db["subscribers"]:

    counter = 0
    for joke in daily:
      await i.send(f"{counter}.{joke}")
      counter += 1
    pass
    #things to do, implement everyone gets 3 jokes a day
    #Create a database of people who needs to get the 3 jokes.
  
'''
  
keep_alive()
client.run(os.getenv("token"))
