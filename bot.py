import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import pytz
from flask import Flask

app = Flask(__name__)
port = 10000

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)


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
    {
        "nom": "HTN",
        "description": "Venez récupérer vos sels quotidiens et vous asseoir sur le trône du royaume des ogres !\nViendrez-vous à bout du Roi Gordok ?",
        "localisation": "Féralas - Kalimdor",
        "requis": "au moins une Clé en croissant dans le groupe",
        "opportunites": "buffs HT, livres HT\nRequis pour run Tribut : une Puissante charge d’hydroglycérine (Ingé) OU une Clé en vrai-argent (Forge) OU un voleur (crochetage 285 minimum)"
    },
    {
        "nom": "UBRS",
        "description": "Venez récupérer vos sels quotidiens et vous frotter aux écailles des draconides noirs !\nViendrez-vous à bout de l’imposant Général Drakkisath ?",
        "localisation": "Mont Blackrock - Royaumes de l’Est",
        "requis": "au moins un sceau d’ascension (clé) dans le groupe / 10 joueurs",
        "opportunites": "tête de Rend (WB), accès BWL\nInvocation : Seigneur Valthalak"
    },
    {
        "nom": "Strat Eca",
        "description": "Venez récupérer vos sels quotidiens et vous confronter à l’inquisition de la Croisade Écarlate !\nViendrez-vous à bout du Grand croisé Dathrohan et de son sombre secret ?",
        "localisation": "Maleterres de l’est - Royaumes de l’Est",
        "requis": "au moins une Clé de la ville si vous passez par l’entrée de service",
        "opportunites": "orbe de piété\nInvocation : Jarien & Sothos"
    },
    {
        "nom": "LBRS",
        "description": "Venez récupérer vos sels quotidiens et déloger les orcs et les ogres réfugiés dans le Mont Blackrock !\nViendrez-vous à bout du Seigneur Wyrmthalak ?",
        "localisation": "Mont Blackrock - Royaumes de l’Est",
        "opportunites": "début de l’accès Onyxia, fragments du sceau d’ascension (clé UBRS)\nInvocation : Mor Grayhoof"
    },
    {
        "nom": "HTE",
        "description": "Venez récupérer vos sels quotidiens et vous mettre au vert le temps d’une instance !\nViendrez-vous à bout d’Alzzin le Modeleur ?",
        "localisation": "Féralas - Kalimdor",
        "opportunites": "Clé en croissant (run Pusilin), essence de vie, livres HT\nInvocation : Isalien"
    },
    {
        "nom": "Strat Baron",
        "description": "Venez récupérer vos sels quotidiens et appréciez la décrépitude et les lamentations des morts-vivants !\nViendrez-vous à bout du Baron Rivendare ?",
        "localisation": "Maleterres de l’est - Royaumes de l’Est",
        "requis": "au moins une Clé de la ville",
        "opportunites": "réputation Aube d’Argent, monture du Baron Rivendare"
    },
    {
        "nom": "Scholomance",
        "description": "Venez récupérer vos sels quotidiens et vous essayer aux enseignements de la nécromancie !\nViendrez-vous à bout du Sombre Maitre Gandling ?",
        "localisation": "Maleterres de l’ouest - Royaumes de l’Est",
        "requis": "au moins une Clé squelette dans le groupe / au moins un caster AOE",
        "opportunites": "runes ténébreuses, peau des ombres, accès au labo pour le craft des flask\nInvocation : Kormok"
    },
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
bot.run('MTMwMjk1MDAzNzk3Mzg5NzIzNg.G65YnW.ABiCWV6FdPBc4grE86woCrxxRdBM8NCEpxhw_k')
