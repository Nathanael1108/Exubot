
################################
############ EXUBOT ############
######### Version 1.0 ##########
###### Maintenue par Nate ######
################################

#################################
###### IMPORT DES MODULES #######
#################################

import os
import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive

keep_alive()  # Lance le serveur web pour maintenir le bot actif

##############################
###### NOMS DIRECTIONS #######
##############################

dir = "Lilou"
codir = "Loïc"
gestionbot = "Nate"
secretaire = "Libre"
dirphoto = "Mathis"
codirphoto = "Théo"
dirjournal = "Maxime"
codirjournal = "Solène"
dirprod = "Libre"
dirDJ = "Matt"
codirDJ = "Nathanael"
dirpodcast = "Maxence"
codirpodcast = "Clémence"

#############################
###### INITIALISATION #######
#############################

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

###############################
###### COMMANDES DU BOT #######
###############################

###########################
###### TEST DE BASE #######
###########################

@bot.command(help="Dit bonjour au monde.")
async def hello(ctx):
    await ctx.send(f"Hello, world! {ctx.author}")

###########################
###### PRESENTATION #######
###########################

@bot.command(name="presentation", help="Le bot se présente.")
async def presentation(ctx):

    await ctx.message.delete()

    embed = discord.Embed(
        title="🤖 Présentation d'Exubot",
        description=(
            "Salut, moi c'est **Exubot**! Enchanté de te rencontrer.\n\n"
            "Tu me verras souvent parler car j'adore ça! "
            "Mais en bref, je suis là comme larbin pour vos directeurs "
            "(Grrrr...) et faire une partie du travail à leur place :)\n\n"
            f"Si tu as besoin de quoi que ce soit, contacte mon créateur 👉 @{gestionbot}.\n\n"
            "Merci!"
        ),
        color=discord.Color.blurple()
    )

    if bot.user.avatar:
        embed.set_thumbnail(url=bot.user.avatar.url)

    embed.set_footer(text="Ton assistant préféré ✨")

    await ctx.send(embed=embed)

###############################################
###### CREATION D'ANNONCE DES REUNIONS ########
###############################################

@bot.command(
    help="SVP ne pas spammez, que pour secrétaire!",
    description="Genere le message pour l'annonce des réunions."
)
async def odj(ctx):

    await ctx.message.delete()

    msg = await ctx.send(
        """Bonjour tout le monde :

🚨 **Réunion hebdomadaire** 🚨  
🕙 **Heure :** 18h15    
📍 **Salle :** Préciser ci-dessous.
👥 : @everyone  

Réagissez avec ✅ si vous serez présent, ❌ si non présent et 💻 si à distance.

**Note :** La réunion est maintenue si au moins 3 personnes sont présentes.

Passez une agréable journée ☀️"""
    )

    await msg.add_reaction("✅")
    await msg.add_reaction("❌")
    await msg.add_reaction("💻")

###########################
###### INFO DU CLUB #######
###########################

@bot.tree.command(name="info", description="Affiche les informations du club")
async def info(interaction: discord.Interaction):

    description = (
        f"⚓ **Capitaine de club** : {dir}\n"
        f"🧭 **Co-capitaine** : {codir}\n"
        f"📝 **Secrétaire / assistant direction** : {secretaire}\n"
        f"📷 **Directeur photo** : {dirphoto}\n"
        f"🤳 **Co-directeur photo** : {codirphoto}\n"
        f"🎛️ **Directeur DJ** : {dirDJ}\n"
        f"🎚️ **Co-directeur DJ** : {codirDJ}\n"
        f"🗞️ **Directeur journal** : {dirjournal}\n"
        f"📰 **Co-directeur journal** : {codirjournal}\n"
        f"💽 **Directeur production** : {dirprod}\n\n"
        f"🎤 **Directeur podcast** : {dirpodcast}\n"
        f"🎙️ **Co-directeur podcast** : {codirpodcast}\n\n"
        "📢 Communication auto-gérée entre pôles."
    )

    footer_text = (
        f"❓ Pour toutes questions, demande sur le #general "
        f"ou ping @{gestionbot}. Merci!"
    )

    embed = discord.Embed(
        title="📣 Informations du club",
        description=description,
        color=discord.Color.gold()
    )

    embed.set_footer(text=footer_text)

    await interaction.response.send_message(embed=embed)

#########################################
###### LIEN DU MESSENGER ################
#########################################

lien_mess = "https://www.messenger.com/cm/AbYcqd3SvUQBmAtq/?send_source=cm%3Adirect_invite_group"

@bot.tree.command(
    name="messenger",
    description="Donne l'invit du messenger en privé."
)
async def messenger(interaction: discord.Interaction):

    await interaction.response.send_message(
        f"Voilà le lien du Messenger : {lien_mess}",
        ephemeral=True
    )

######################################################
###### COMMANDES POUR LE RESUME DE REUNION ###########
######################################################

@bot.tree.command(
    name="resreu",
    description="Affiche le prompt ChatGPT"
)
async def resume(interaction: discord.Interaction):

    await interaction.response.send_message(
        content=(
            '''Voici le prompt Chat-GPT que tu peux utiliser :

`Dans le but de clarifier les communications, je souhaite faire de beau compte rendu de réunion. Mets en forme mes notes sous la forme d'un compte rendu de réunion propre et clair. Voici ma prise de note : "Coller le texte du résumé ici"`'''
        ),
        ephemeral=True
    )

##########################################
###### FONCTIONS RAPPELS PÔLES ###########
##########################################

@bot.command(
    help="Informe que le resume de reunion est dispo."
)
async def resumereudispo(ctx):

    await ctx.message.delete()

    await ctx.send(
        """**Résumé de réunion disponible!**  
@everyone 

Salut tout le monde, le résumé de notre dernière réunion est disponible!

Tu peux le retrouver ici :arrow_right: #résumé-réunion.

Bonne journée!"""
    )

@bot.command(
    help="Rappelez aux photographe de déposer leur photos."
)
async def rappelphoto(ctx):

    await ctx.message.delete()

    await ctx.send(
        """📸 **Rappel Photo**  
@Photo/Vidéo  

Salut tout le monde !

🗓️ **Pensez à déposer vos photos de votre dernière prestation** dans le dossier prévu.  

📁 **Lien du Sharepoint :**  
https://aeets0.sharepoint.com/sites/exutoire/Documents%20partages/Forms/AllItems.aspx?id=%2Fsites%2Fexutoire%2FDocuments%20partages%2FPhotos%2FEvenements&viewid=cada9721%2D109e%2D443b%2Dbabb%2D578be683514b

🕐 **Deadline :** Deux semaines max après la fin de l'évenement!

Merci à tous pour votre participation 🙌"""
    )

@bot.command(
    help="Informer les photographes des nouvelles prestas."
)
async def rappelpresta(ctx):

    await ctx.message.delete()

    await ctx.send(
        """📷 **Nouvelle(s) prestas!**  
@Photo/Vidéo

Salut tout le monde, on a une ou plusieurs presta(s) de prévue bientôt!

**Si t'es dispo et intéressé**, réagis avec ✅ sur l'événement correspondant dans #évènements-à-venir-photo.

Merci à tous pour votre participation 🙌"""
    )

@bot.command(
    help="Rappelez aux DJs qu'un évent arrive."
)
async def rappeldj(ctx):

    await ctx.message.delete()

    await ctx.send(
        """🎛️ **Rappel DJ**  
@DJ 

Salut tout le monde, on a un ou plusieurs event(s) de prévu bientôt!

**Si t'es dispo et intéressé**, réagis avec ✅ sur l'événement correspondant dans #évènements-à-venir-dj.

Merci à tous pour votre participation 🙌"""
    )

@bot.command(
    help="Rappelez qu'il y a une réunion."
)
async def rappelreu(ctx):

    await ctx.message.delete()

    await ctx.send(
        """⚠️ **==[Rappel reunion]==** ⚠️

||@everyone||

Salut tout le monde, pour rappel rencontre de club ce **jeudi à 17h30.**

Si tu l'as pas déjà fait, hésites pas à réagir au message :arrow_up:

Merci à tous pour votre participation 🙌"""
    )

############################################
###### FONCTIONS POLES PROD / DJ ###########
############################################

@bot.tree.command(
    name="partageset",
    description="Publie un nouveau set avec un lien"
)
@app_commands.describe(url="Lien vers le set à partager")
async def partageset(interaction: discord.Interaction, url: str):

    user = interaction.user.mention

    await interaction.response.send_message(
        f"{user} a publié un nouveau set! 🎧\n"
        f"Tu peux le retrouver ici: {url}\n\n"
        f"Enjoy!"
    )

@bot.tree.command(
    name="partageson",
    description="Publie un nouveau son avec un lien"
)
@app_commands.describe(url="Lien vers le son à partager")
async def partageson(interaction: discord.Interaction, url: str):

    user = interaction.user.mention

    await interaction.response.send_message(
        f"{user} a publié un nouveau son! 🎵\n"
        f"Tu peux le retrouver ici: {url}\n\n"
        f"Enjoy!"
    )

###########################################
###### SURVEILLANCE DES EMPRUNTS ##########
###########################################

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.Thread):

        parent = message.channel.parent

        if parent and parent.name == "emprunt-test":

            await parent.send(
                f"📣 Nouveau message dans le post "
                f"**{message.channel.name}** "
                f"par {message.author.mention} !"
            )

    await bot.process_commands(message)

###########################################
############## READY EVENT ################
###########################################

@bot.event
async def on_ready():

    print(f"Bot prêt - connecté en tant que {bot.user}")

    await bot.tree.sync()

    print("Commandes slash synchronisées")

###########################################
############ DEMARRAGE BOT ################
###########################################

token = os.environ['TOKEN_BOT']
bot.run(token)

