################################
############ EXUBOT ############
######### Version 0.6 ##########
###### Maintenue par Nate ######
################################

#################################
###### IMPORT DES MODULES #######
#################################

import os
import discord
from discord.ext import commands
from discord import app_commands
import requests
from datetime import datetime, timedelta
from keep_alive import keep_alive
from fpdf import FPDF
import io

keep_alive()  #Lance le serveur web pour maintenir le bot actif

##############################
###### NOMS DIRECTIONS #######
##############################

dir = "Emile"
codir = "Xavier"
gestionbot = "Secrétaire"
secretaire = "Nathanael"
dirphoto = "Julia"
codirphoto = "Valentine"
dirjournal = "Alan"
codirjournal = "Pierre"
dirprod = "Libre"
dirDJ = "Matt"
codirDJ = "Alban"

#############################
###### INITIALISATION #######
#############################

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.members = True #Pour avoir accès à la liste des membres
intents.presences = True #Voir les status des membres
#intents.threads = True  # 🔥 Ce flag est important
bot = commands.Bot(command_prefix='!', intents=intents)

########################################
###### DICTIONNAIRE JOURS / MOIS #######
########################################

jours_fr = [
    'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'
]
mois_fr = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août',
    'Septembre', 'Octobre', 'Novembre', 'Décembre'
]

###############################
###### COMMANDES DU BOT #######
###############################

###########################
###### TEST DE BASE #######
###########################


@bot.command(help="Dit bonjour au monde.",
             description="Dit bonjour au monde poliment.")
async def hello(ctx):
  await ctx.send(f"Hello, world! {ctx.author}")

###########################
###### PRESENTATION #######
###########################

@bot.command(name="presentation", help="Le bot se présente.")
async def presentation(ctx):
    # Supprime le message de commande
    await ctx.message.delete()

    embed = discord.Embed(
        title="🤖 Présentation d'Exubot",
        description=(
            "Salut, moi c'est **Exubot**! Enchanté de te rencontrer.\n\n"
            "Tu me verras souvent parler car j'adore ça! Mais en bref, "
            "je suis là comme larbin pour votre secrétaire (Grrrr...) "
            "et faire une partie du travail à sa place :)\n\n"
            "Si tu as besoin de quoi que ce soit, contacte mon créateur 👉 @Secrétaire.\n\n"
            "Merci!"
        ),
        color=discord.Color.blurple()
    )

    # Ajout de l’avatar du bot en miniature
    if bot.user.avatar:
        embed.set_thumbnail(url=bot.user.avatar.url)

    embed.set_footer(text="Ton assistant préféré ✨")

    await ctx.send(embed=embed)

########################################
###### OBTENTION DATE NEXT JEUDI #######
########################################


def get_next_thursday_fr():
  today = datetime.today()
  days_ahead = (3 - today.weekday() + 7) % 7
  if days_ahead == 0:
    days_ahead = 7  # On saute au jeudi suivant si on est jeudi
  next_thursday = today + timedelta(days=days_ahead)
  jour = jours_fr[next_thursday.weekday()]
  jour_num = next_thursday.day
  mois = mois_fr[next_thursday.month - 1]

  return f"{jour} {jour_num} {mois}"


###############################################
###### CREATION D'ANNONCE ORDRE DU JOUR #######
###############################################


class OdjView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(label="📋 Voir l'ordre du jour",
                     style=discord.ButtonStyle.primary)
  async def show_odj(self, interaction: discord.Interaction,
                     button: discord.ui.Button):
    url = "https://mensuel.framapad.org/p/Reunion_Exutoire/export/txt"
    response = requests.get(url)

    if response.status_code != 200:
      await interaction.response.send_message(
          "❌ Impossible de récupérer l'ordre du jour.", ephemeral=True)
      return

    content = response.text
    lines = content.splitlines()

    inside_block = False
    extracted_lines = []

    for line in lines:
      if "—————BEGIN——————" in line:
        inside_block = True
        continue
      elif "—————STOP——————" in line:
        break
      if inside_block:
        extracted_lines.append(line)

    # Affichage du texte
    extracted_text = "\n".join(extracted_lines).strip()
    if len(extracted_text) > 1900:
      extracted_text = extracted_text[:1900]

    first_line = lines[0] if len(lines) > 0 else ""
    message = f"*{first_line}**\n{extracted_text}"

    await interaction.response.send_message(content=f'''📄 **Ordre du jour :**
**➡️ Pour ajouter un point :** [Clique ici](https://mensuel.framapad.org/p/Reunion_Exutoire)
```{message}```''',
                                            ephemeral=True)


# Commande classique avec bouton
@bot.command(help="SVP ne pas spammez, que pour secrétaire!",
             description="Genere le message pour l'annonce des réunions.")
async def odj(ctx):
  await ctx.message.delete()
  jeudi = get_next_thursday_fr()

  msg = await ctx.send(f"""Bonjour tout le monde :

🚨 **Réunion hebdomadaire** 🚨  
📆 **Date :** {jeudi}   
🕙 **Heure :** 17h30    
📍 **Salle :** Salle D-3012 (ou autres si petit nombre)  
👥 : @everyone  
📝 Ordre du jour : Cliquez sur le bouton ci-dessous.  
Réagissez avec ✅ si vous serez présent, ❌ si non présent et 💻 si à distance.
**Note :** La réunion est maintenue si au moins 3 personnes sont présentes.\n  
Passez une agréable journée ☀️""",
                       view=OdjView())

  # Ajout des réactions
  await msg.add_reaction("✅")
  await msg.add_reaction("❌")
  await msg.add_reaction("💻")

#Envoi ordre du jour en mp a celui qui demande

@bot.command(name="odjmp")
async def odjmp(ctx):
    url = "https://mensuel.framapad.org/p/Reunion_Exutoire/export/txt"
    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
        lines = content.splitlines()

        inside_block = False
        extracted_lines = []

        for line in lines:
            if "—————BEGIN——————" in line:
                inside_block = True
                continue
            elif "—————STOP——————" in line:
                break
            if inside_block:
                extracted_lines.append(line)

        texte = "\n".join(extracted_lines).strip()

        if texte:
            # Tronquer si trop long
            if len(texte) > 1900:
                texte = texte[:1900] + "\n\n⚠️ (tronqué pour respecter la limite Discord)"

            try:
                await ctx.author.send(texte)
            except:
                pass  # on ignore s'il ne peut pas envoyer de MP

# Annonce de la reunion pour le messenger

@bot.tree.command(name="odjmess", description="Annonce formatée pour Messenger")
async def odjmess(interaction: discord.Interaction):
    jeudi = get_next_thursday_fr()

    message_messenger = (
        f"Bonjour tout le monde :\n\n"
        f"🚨 *Réunion hebdomadaire* 🚨\n"
        f"📆 *Date :* {jeudi}\n"
        f"🕙 *Heure :* 17h30\n"
        f"📍 *Salle :* D-3012\n"
        f"👥 *@everyone*\n"
        f"📝 *Ordre du jour :* S'en vient à la suite de ce message.\n"
        f"Réagissez avec 👍 si vous serez présent, 👎 si non présent et 💻 si à distance.\n\n"
        f"*Note :* La réunion est maintenue si au moins 3 personnes sont présentes.\n\n"
        f"Passez une agréable journée ☀️"
    )


######################################
###### SONDAGE DISPO RENCONTRE #######
######################################

# Non utilisé pour le moment

@bot.command(help="Sondage pour dispo réunion.",
             description="Genere le sondage pour capter les dispos pour les réunions.")
async def dispo(ctx):
  await ctx.message.delete()
  options = [
      "1️⃣ Lundi - 17h30", "2️⃣ Mardi - 17h30", "3️⃣ Mercredi - 17h30",
      "4️⃣ Jeudi - 17h30", "5️⃣ Vendredi - 17h30", "6️⃣ Week-end - À définir"
  ]

  # Crée le message du sondage
  description = "\n".join(options)
  embed = discord.Embed(title="📅 Sondage - Quel jour pour les rencontres ?",
                        description=description,
                        color=discord.Color.red())
  embed.set_footer(text="Reagis avec le choix correspondant.")

  message = await ctx.send(embed=embed)

  # Ajoute les réactions correspondantes
  emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
  for emoji in emojis:
    await message.add_reaction(emoji)


###########################
###### INFO DU CLUB #######
###########################


@bot.tree.command(name="info", description="Affiche les informations du club")
async def info(interaction: discord.Interaction):
  description = (f"⚓ **Capitaine de club** : {dir}\n"
                 f"🧭 **Co-capitaine** : {codir}\n"
                 f"📝 **Secrétaire / assistant direction** : {secretaire}\n"
                 f"📷 **Directrice photo** : {dirphoto}\n"
                 f"🤳 **Co-directrice photo** : {codirphoto}\n"
                 f"🎛️ **Directeur DJ** : {dirDJ}\n"
                 f"🎚️ **Co-directeur DJ** : {codirDJ}\n"
                 f"🗞️ **Directeur journal** : {dirjournal}\n"
                 f"📰 **Co-directeur journal** : {codirjournal}\n"
                 f"💽 **Directeur production** : {dirprod}\n\n"
                 "🎙️ Le pôle podcast va sûrement repartir.\n"
                 "📢 Communication auto-gérée entre pôles ou le pôle va renaître.")

  footer_text = f"❓ Pour toutes questions, demande sur le #general ou ping @{gestionbot}. Merci!"

  embed = discord.Embed(title="📣 Informations du club",
                        description=description,
                        color=discord.Color.gold())
  embed.set_footer(text=footer_text)

  # Envoi éphémère (visible uniquement par l'utilisateur)
  await interaction.response.send_message(embed=embed, ephemeral=True)

#Fonction du lien d'invit du messenger

lien_mess = "https://www.messenger.com/cm/AbYcqd3SvUQBmAtq/?send_source=cm%3Adirect_invite_group" #Lien du messenger, a update si expiré

# Slash commande qui envoie un lien en ephemeral
@bot.tree.command(name="messenger", description="Donne l'invit du messenger en privé (ephemeral).")
async def messenger(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Voilà le lien du Messenger : {lien_mess}",
        ephemeral=True
    )

######################################################
###### COMMANDES POUR LE RESUME DE REUNION ###########
######################################################


@bot.tree.command(name="resreu", description="Affiche le résumé de la réunion")
async def resume(interaction: discord.Interaction):
  url = "https://mensuel.framapad.org/p/Reunion_Exutoire/export/txt"
  response = requests.get(url)

  if response.status_code != 200:
    await interaction.response.send_message(
        "❌ Impossible de récupérer le pad.", ephemeral=True)
    return

  content = response.text
  lines = content.splitlines()

  # Extraire les lignes entre les balises
  inside_block = False
  extracted_lines = []

  for line in lines:
    if "—————DEBUT——————" in line:
      inside_block = True
      continue
    elif "—————FIN——————" in line:
      break
    if inside_block:
      extracted_lines.append(line)

  extracted_text = "\n".join(extracted_lines).strip()

  # Tronquer si trop long
  if len(extracted_text) > 1900:
    extracted_text = extracted_text[:1900]

  message = f"**📝 Texte à copier coller :**\n```{extracted_text}```"

  await interaction.response.send_message(content=message, ephemeral=True)
  await interaction.followup.send(
      content=
      '''**Prompt ChatGPT :** `Dans le but de clarifier les communications, je souhaite faire de beau compte rendu de réunion. Mets en forme mes notes sous la forme d'un compte rendu de réunion propre et clair. Fournis moi ton travail en markdown sans aucun marqueur de formatage. Voici l'ordre du jour "Coller l'ordre du jour ici" et ma prise de note : "Coller le texte du résumé ici"`''',
      ephemeral=True)


##########################################
###### FONCTIONS RAPPELS PÔLES ###########
##########################################
'''#Rappels template
@bot.command(help="Message d'aide.",
             description="Desc.")
async def rappel(ctx):
  await ctx.message.delete()

  await ctx.send("""**Rappel Role**  
@Role 
Salut tout le monde, [SAISIR TEXTE ICI]!
[SAISIR TEXTE ICI]
Merci à tous pour votre participation 🙌""")'''

#Rappels resume de reu
@bot.command(help="Informe que le resume de reunion est dispo.",
             description="Informe avec un piti everyone.")
async def resumereudispo(ctx):
  await ctx.message.delete()

  await ctx.send("""**Résumé de réunion disponible!**  
@everyone 
Salut tout le monde, le résumé de notre dernière réunion est disponible!
Tu peux le retrouver ici :arrow_right: #résumé-réunion.
Bonne journée!""")

#Rappels depots photos
@bot.command(help="Rappelez aux photographe de déposer leur photos.",
             description="Rappel avec lien sharepoint.")
async def rappelphoto(ctx):
  await ctx.message.delete()

  await ctx.send("""📸 **Rappel Photo**  
@Photo/Vidéo  
Salut tout le monde !

🗓️ **Pensez à déposer vos photos de votre dernière prestation** dans le dossier prévu.  

📁 **Lien du Sharepoint :** [Sharepoint](https://aeets0.sharepoint.com/sites/exutoire/Documents%20partages/Forms/AllItems.aspx?id=%2Fsites%2Fexutoire%2FDocuments%20partages%2FPhotos%2FEvenements&viewid=cada9721%2D109e%2D443b%2Dbabb%2D578be683514b)  
🕐 **Deadline :** Deux semaines max après la fin de l'évenement!

Merci à tous pour votre participation 🙌""")

#Rappels nouvelles prestas photo
@bot.command(help="Informer les photographes des nouvelles prestas.",
             description="Informe que des nouvelles prestas sont la.")
async def rappelpresta(ctx):
  await ctx.message.delete()

  await ctx.send("""📷 **Nouvelle(s) prestas!**  
@Photo/Vidéo
Salut tout le monde, on a une ou plusieurs presta(s) de prévue bientôt!

**Si t'es dispo et intéressé**, réagis avec ✅ sur l'événement correspondant dans #évènements-à-venir-photo.
Merci à tous pour votre participation 🙌""")


#Rappels dj
@bot.command(help="Rappelez aux DJs qu'un évent arrive.",
             description="Rappel dj avec indication case verte à cocher.")
async def rappeldj(ctx):
  await ctx.message.delete()

  await ctx.send("""🎛️ **Rappel DJ**  
@DJ 
Salut tout le monde, on a un ou plusieurs event(s) de prévu bientôt!

**Si t'es dispo et intéressé**, réagis avec ✅ sur l'événement correspondant dans #évènements-à-venir-dj.
Merci à tous pour votre participation 🙌""")


@bot.command(help="Rappelez qu'il y a une réunion.",
             description="Rappel avec ping de everyone.")
async def rappelreu(ctx):
  await ctx.message.delete()

  await ctx.send("""⚠️**==[Rappel reunion]==**⚠️\n
||@everyone|| 
Salut tout le monde, pour rappel rencontre de club ce **jeudi à 17h30.**
Si tu l'as pas déjà fait, hésites pas à réagir au message :arrow_up: 
Merci à tous pour votre participation 🙌""")


############################################
###### FONCTIONS POLES PROD / DJ ###########
############################################


#Publication de set
@bot.tree.command(name="partageset",
                  description="Publie un nouveau set avec un lien")
@app_commands.describe(url="Lien vers le set à partager")
async def partageset(interaction: discord.Interaction, url: str):
  user = interaction.user.mention
  await interaction.response.send_message(
      f"{user} a publié un nouveau set! 🎧 Tu peux le retrouver ici: {url} \nEnjoy!"
  )


#Publication de son
@bot.tree.command(name="partageson",
                  description="Publie un nouveau son avec un lien")
@app_commands.describe(url="Lien vers le son à partager")
async def partageson(interaction: discord.Interaction, url: str):
  user = interaction.user.mention
  await interaction.response.send_message(
      f"{user} a publié un nouveau son! 🎵 Tu peux le retrouver ici: {url} \nEnjoy!"
  )


###########################################
###### SURVEILLANCE DES EMPRUNTS ##########
###########################################

#En développement - pas sur qu'il y aura une version finale

@bot.event
async def on_message(message):
    # Ignore les messages du bot
    if message.author == bot.user:
        return

    # Vérifie si le message est dans un thread rattaché à un forum
    if isinstance(message.channel, discord.Thread):
        parent = message.channel.parent
        if parent and parent.name == "emprunt-test":
            await parent.send(f"📣 Nouveau message dans le post **{message.channel.name}** par {message.author.mention} !")

    await bot.process_commands(message)


##########################################
###### CREATION PDF RESUME REUNION #######
##########################################


# Modal personnalisé pour saisir le texte
class PdfModal(discord.ui.Modal, title="Texte pour PDF"):
  texte = discord.ui.TextInput(
      label="Écris ton texte ici",
      style=discord.TextStyle.paragraph,  # multi-lignes
      placeholder="Tape ton texte...",
      max_length=4000,
      required=True)

  def __init__(self, interaction):
    super().__init__()
    self.interaction = interaction

  async def on_submit(self, interaction: discord.Interaction):
    # Nettoyage simple des caractères spéciaux
    texte_nettoye = self.texte.value.replace("’",
                                             "'").replace("–", "-").replace(
                                                 "“", '"').replace("”", '"')

    # Création PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in texte_nettoye.splitlines():
      pdf.multi_cell(0, 10, line)

    pdf_bytes = io.BytesIO()
    pdf_data = pdf.output(dest='S').encode('latin1')
    pdf_bytes.write(pdf_data)
    pdf_bytes.seek(0)

    #Nom du fichier
    Nomfich = "Resume_de_la_reunion_precedente.pdf"

    await interaction.response.send_message(content="📄 Voici ton PDF :",
                                            file=discord.File(
                                                pdf_bytes, filename=Nomfich),
                                            ephemeral=True)


# Commande slash qui appelle le modal
@bot.tree.command(
    name="makepdf",
    description="Crée un PDF à partir d'un texte via un formulaire")
async def makepdf(interaction: discord.Interaction):
  modal = PdfModal(interaction)
  await interaction.response.send_modal(modal)


##NE PAS SUPPRIMER CE QU'IL Y A CI-DESSOUS##


@bot.event
async def on_ready():
  print(f"Bot prêt - connecté en tant que {bot.user}")
  # Synchronise les commandes slash globalement
  await bot.tree.sync()
  print("Commandes slash synchronisées")


#Appel et démarrage du bot
token = os.environ['TOKEN_BOT']
bot.run(token)
