import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz
import asyncio
from flask import Flask

app = Flask(__name__)
port = 10000

@app.route('/')
def hello_world():
    return 'Hello World!'

# Configuration du bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Liste des instances dans l'ordre donné
instances = [
    {
        "nom": "BRD",
        "description": "Venez récupérer vos sels quotidiens et vous réchauffer dans les bassins de lave du Mont Blackrock !\nViendrez-vous à bout de l’empereur Dagran Thaurissan ?",
        "localisation": "Mont Blackrock - Royaumes de l’Est",
        "requis": "au moins une clé ombreforge dans le groupe",
        "opportunites": "fonte du sombrefer, accès MC"
    },
    # Ajoutez ici les autres instances...
    {
        "nom": "HTO",
        "description": "Venez récupérer vos sels quotidiens et bouquiner dans la bibliothèque d’Eldre’Thalas !\nViendrez-vous à bout du Prince Tortheldrin ?",
        "localisation": "Féralas - Kalimdor",
        "requis": "au moins une Clé en croissant dans le groupe",
        "opportunites": "essence de vie, livres HT, enchantements HT"
    }
]

# Index de l'instance actuelle
current_instance_index = 4

# Fonction pour envoyer l'annonce quotidienne
async def send_instance(channel):
    global current_instance_index
    
    instance = instances[current_instance_index]
    message = (
        f"**Instance du jour : {instance['nom']}**\n\n"
        f"{instance['description']}\n\n"
        f"Localisation : {instance['localisation']}\n"
        f"Requis : {instance.get('requis', 'Aucun')}\n"
        f"Opportunité(s) : {instance['opportunites']}\n"
    )

    await channel.send(message)

    # Mise à jour de l'index pour le prochain jour
    current_instance_index = (current_instance_index + 1) % len(instances)

# Tâche pour l'annonce quotidienne
@tasks.loop(minutes=1)
async def daily_instance():
    channel = bot.get_channel(1296490530099822685)  # Remplacez par l'ID de votre canal
    now = datetime.now(pytz.timezone('Europe/Paris'))  # Changez le fuseau horaire si nécessaire

    if now.hour == 7 and now.minute == 0:  # À 7h du matin
        await send_instance(channel)
        await asyncio.sleep(60)  # Évite les répétitions dans la même minute

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')
    daily_instance.start()  # Démarre l'annonce quotidienne

# Remplacez 'YOUR_TOKEN' par le token de votre bot
bot.run('MTMwMjk1MDAzNzk3Mzg5NzIzNg.GGP8yX.DNj6NYLl4NxhhAEjL78OoSpkP1kNpud-K93V1k')  # Remplacez par votre token
