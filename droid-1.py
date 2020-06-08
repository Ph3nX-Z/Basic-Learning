#################################################
# IA by Ph3nX-Z : https://github.com/Ph3nX-Z/   #
#################################################

import csv
import pandas as panda
import sys
import time

file_creation=open("user.txt","a") #evite les erreurs du style : ce fichier est introuvable ...
file_creation.close()
file_creation2=open("reponses.csv","a")
file_creation2.close()


def bye():
    print("Bot >>Goodbye Sir")
    time.sleep(4)
    sys.exit()

def speech(something): #voix tres creepy (pas celle utilisée)
    import pyttsx3
    speaker=pyttsx3.init()
    speaker.setProperty('rate',70)
    voices=speaker.getProperty('voices')
    print(voices)
    speaker.setProperty('voices', voices[1].id)
    speaker.say(something)
    speaker.runAndWait()

def speech2(something): #voix moins creepy
    from gtts import gTTS
    import playsound
    tts=gTTS(text=something)
    tts.save("speech.mp3")
    playsound.playsound('speech.mp3',True)

def getuser(): # check si un user a deja été ajouté
    user_file=open("user.txt", "r+")
    user=user_file.read()
    if user=='':
        user_new=input("What's your name :")
        user_file.write(user_new)
        user_file.close()
        return user_new
    else:
        user_file.close()
        return user

def write_header():  #ecrit le nom des colonnes
    f=open("reponses.csv","a")
    colonnes= ['question','reponse']
    writer=csv.DictWriter(f, fieldnames=colonnes)
    writer.writeheader()
    f.close()

header=("question,reponse")

test=open("reponses.csv",'r')
content=test.read()
occurences=content.count(header) #verifie si le nom des colonnes est present dans le fichier
if occurences==0:
    write_header()

user=getuser() #ecrit votre nom dans un fichier txt
question=input(user+" >>") 
question=question.upper()
if question=='EXIT':
    bye()
elif question=='BYE':
    bye()
elif question=='GOODBYE':
    bye()


def enter_reponse():
    search=panda.read_csv("reponses.csv", delimiter=';') #regarder si la question a deja été posée
    word=question ## a la longue faire en sorte de trouver celui qui a les mots les plus proches (le plus de lettres en commun)
    file=open("reponses.csv",'r')
    data=file.read()
    count=data.count(question)
    count=int(count)
    if count>0:
        return False
    elif count==0:
        return True


def write(question, reponse): #si la question n'as jamais été posée elle est ajoutée au fichier csv
    with open("reponses.csv","a") as csv_file:
        colonnes= ['question','reponse']
        writer=csv.DictWriter(csv_file, fieldnames=colonnes)
        writer.writerow({'question':question, "reponse":reponse})

enter_rep=enter_reponse() #resultat du enter reponse + savoir si il faut ajouter le mot a la base
if enter_rep==True:
    reponse=input("I don't know sir, please tell me what's the reponse :")
    write(question,reponse) #fonction pour ecrire dans le fichier (a regarder plus haut)
else :
    ###get csv correspondant a la question
    f=open("reponses.csv",'r')
    dico=f.read()
    for item in dico.split("\n") :
        if question in item:
            line_data=item.strip()
    list=line_data.split(',')
    reponse_bot=list[1]
    print("Bot >>"+reponse_bot)
    try:
        speech2(reponse_bot)
    except:
        print("No internet connection = no voice !") #la voix google ne fonctionnera pas sans acces internet (en enlevant le 2 derriere le speech (juste la ligne d'au dessus)on reactive la voix creepy (pas besoin de co) )

#errors : aplay : sudo apt-get install alsa-utils
#pas encore de loop mais je l'ajouterais bientot ^^