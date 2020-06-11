# coding=cp1252
#################################################
# IA by Ph3nX-Z : https://github.com/Ph3nX-Z/   #
#################################################

import csv
import pandas as panda
import sys
import time
import os

hamming_method=False
question_regroupee=""
speakmode=False
learnmode=False
choix=False
passnext=False
speak_turn=False
enter_rep=False
continu=False
mini_start=1000

file_creation=open("user.txt","a") #evite les erreurs du style : ce fichier est introuvable ...
file_creation.close()
file_creation2=open("reponses.csv","a")
file_creation2.close()

def mot_clef(database_input,question):
    compteur=0
    database_input_split=database_input.split(" ")

    question_splitted=question.split(" ")
    for data_sort in question_splitted:
        for data_sort2 in database_input_split:
            if data_sort==data_sort2:
                compteur+=1

    return compteur

def hamming(a, b):
    distance=0
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            distance+=1
    return distance



def processing(test,question):

    minimal=0
    temp=0
    mot_final=""
    reponse_temp=""
    liste=test.split(",")
    question_finale=""
    mot_entier=""
    minimal=1000
    mot=liste[0]
    mot_split=mot.split(" ")
    question_split=question.split(" ")
    if question_split[0]=="":
        question_split.remove("")
    if question_split[-1]=="":
        question_split.remove("")
    for partie in question_split:
        question_finale+=partie

    for parties in mot_split:
        mot_entier += parties
        reponse_temp=liste[1]
    
    temp=hamming(question_finale,mot_entier)
    if temp < minimal:
        mot_final=reponse_temp
        minimal=temp
        temp_mot_entier=mot_entier
        mot_temp_2=mot

    return mot_final,str(minimal),mot_temp_2




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
    os.remove("speech.mp3")


def bye():
    print("Bot >>Goodbye Sir")
    speech2("Goodbye Sir")
    time.sleep(4)
    sys.exit()
    


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


def enter_reponse():
    return True

def write(question, reponse): #si la question n'as jamais été posée elle est ajoutée au fichier csv
    with open("reponses.csv","a") as csv_file:
        colonnes= ['question','reponse']
        writer=csv.DictWriter(csv_file, fieldnames=colonnes)
        writer.writerow({'question':question, "reponse":reponse})



while True:
    user=getuser() #ecrit votre nom dans un fichier txt
    question=input(user+" >>") 
    question=question.upper()
    if question=='EXIT':
        bye()
    elif question=='BYE':
        bye()
    elif question=='GOODBYE':
        bye()
    elif question=='SPEAK':
        enter_rep=False
        passnext=True
        learnmode=False
        speakmode=True
    elif question=="LEARN":
        enter_rep=True
        learnmode=True
        passnext=True
    elif question=="RECTIFY":
        question=question_cache #se rappeler de la derniere question
        reponse_corrige=input("Bot >>What was the good response to have ? :")
        write(question,reponse_corrige)
        rectify=True
        passnext=True


    if passnext!=True:
        if enter_rep == True:
            enter_rep=enter_reponse() #resultat du enter reponse + savoir si il faut ajouter le mot a la base
        if enter_rep==True: #remettre true 
            reponse=input("I don't know sir, please tell me what's the reponse :")
            write(question,reponse) #fonction pour ecrire dans le fichier (a regarder plus haut)
        else :
            ###get csv correspondant a la question
            f=open("reponses.csv",'r')
            dico=f.read()
            f.close()
            for item in dico.split("\n") :
                if item != "":
                    returned1,returned2,question_cache=processing(item,question)
                    mini=int(returned2)
                    mot_temp=returned1

                    if mini<int(mini_start):
                        hamming_method=True
                        mini_start=mini
                        question_cache_final=question_cache
                        print("mini actuel:"+str(mini))
                        reponse_bot_final=mot_temp
                        

            if hamming_method==True:
                print("Hamming method")
            
            question_splitted_2=question.split(" ")
            for j in range(len(question_splitted_2)):
                question_regroupee+=question_splitted_2[j]

            if len(question_cache_final)!=len(question_regroupee): #######continuer la 
                if mini_start > 1:
                    maxi=0
                    p=open("reponses.csv",'r') #par mot clef
                    dico3=p.read()
                    p.close()
                    for items2 in dico3.split('\n'):
                        if items2 != "":
                            to_func=items2.split(",")
                            reponse_temp=to_func[1]
                            temp=mot_clef(to_func[0], question)
                            if temp>maxi:
                                maxi=temp
                                reponse_bot_final=reponse_temp
                                print("keyword method")

            question_regroupee=""
            m=open("reponses.csv",'r')
            dico2=m.read()
            m.close()
            for item in dico2.split("\n") :  ######trouver un mot exactement similaire
                mots=item.split(",")
                if question==mots[0]:
                    mots2=mots[1]
                    print(mots2)
                    reponse_bot_final=mots2
            print("raw method")
                    
                    

            try :
                print("Bot >>"+reponse_bot_final)
                question_cache=question #garder ancienne question en cache
            except:
                print("No correspondant response in the database, entering in learning mode")
                enter_rep=True
            mini_start=1000
            mot_temp=""
            try:
                speech2(reponse_bot_final)
            except:
                if enter_rep!=True:
                    print("No internet connection = no voice !") #la voix google ne fonctionnera pas sans acces internet (en enlevant le 2 derriere le speech (juste la ligne d'au dessus)on reactive la voix creepy (pas besoin de co) )
                else:
                    print("")    
    if passnext==True:
        if learnmode==True:
            print("Bot >>Switching Mode, Now in LearnMode !")
        elif speakmode==True:
            print("Bot >>Switching Mode, Now in SpeakMode !")
            speakmode=False
        elif rectify==True:
            print("Bot >>I rectified my database !")
            rectify=False
        passnext=False
        hamming_method=False
#errors : aplay : sudo apt-get install alsa-utils
#pas encore de loop mais je l'ajouterais bientot ^^
