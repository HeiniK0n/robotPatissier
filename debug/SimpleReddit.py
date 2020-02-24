# coding: utf8
#!/usr/bin/env python3

from datetime import date
from datetime import datetime
from threading import Thread
from threading import Thread, RLock
from time import sleep
import datetime as dt
import emoji
import os.path
import praw
import sys
import threading
import time


#  ============================

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: `./SimpleReddit parametres` "  
        + " ou parametres est un fichier de type "
        + " `\n nombot "
        + " \n client_id:client_secret "
        + " \n username:password "
        + " \n profondeurPoteau:profondeurCommentaire "
        + " \n sousmarin "
        + " \n fichierDeSauvegarde`")
        sys.exit(-1)

    ID={}
    try:
        with open(sys.argv[1]) as pem:
            for ln, line in enumerate(pem):
                elem = [e.strip() for e in line.strip().split(':')]
                if ln == 0:
                    ID["nom"] = elem[0]
                elif ln == 1:
                    ID["client_id"]     = elem[0]
                    ID["client_secret"] = elem[1]
                elif ln == 2:
                    ID["username"] = elem[0]
                    ID["password"] = elem[1]
                elif ln == 3:
                    ID["profondeurPoteau"] = elem[0]
                    ID["profondeurCommentaire"] = elem[1]
                elif ln == 4:
                    ID["sousmarins"] = elem[0]
                elif ln == 5:
                    ID["NomDuFichierDeSauvegarde"] = elem[0]
    except:
        print("Fichier 'parametres' invalide.")
        print("Usage: `./SimpleReddit parametres` "  
        + " ou parametres est un fichier de type "
        + " `\n nombot "
        + " \n client_id:client_secret "
        + " \n username:password "
        + " \n profondeurPoteau:profondeurCommentaire "
        + " \n sousmarins(séparés par des tirets) "
        + " \n nom du fichier de sauvegarde des gateauisés du jour`")
        sys.exit(-1)

    

    start_time = time.time() 
    print("===============================\n= start : "+time.strftime("%Y-%m-%d %H:%M:%S")+" =\n===============================")        

    

    luceci = praw.Reddit(user_agent=ID["nom"],
                         client_id=ID["client_id"],
                         client_secret=ID["client_secret"],
                         username=ID["username"],
                         password=ID["password"])

    nomRedditeur='Minstaer'

    print( datetime.fromtimestamp((luceci.redditor(nomRedditeur).created_utc)).strftime("%Y-%m-%d") )
    print("created_utc")

    # print( datetime.fromtimestamp((luceci.redditor("nomRedditeur").created)).strftime("%Y-%m-%d") )
    # print("created")

    dt_objectRedditeurCommenteur = datetime.fromtimestamp(luceci.redditor(nomRedditeur).created_utc)

    print( "date depliée" + "/"+ luceci.redditor(nomRedditeur).name + "[" + luceci.redditor(nomRedditeur).id + "] " 
                        + str(dt_objectRedditeurCommenteur.day) + "/" 
                        + str(dt_objectRedditeurCommenteur.month) + "/"
                        + str(dt_objectRedditeurCommenteur.year)     )

   
    print("=============================\n= end : "+time.strftime("%Y-%m-%d %H:%M:%S")+" =\n=============================")
    print("Temps d execution : ",  time.strftime('%H:%M:%S', time.gmtime((time.time() - start_time))))

    print("======== AUREVOIR ===========")  
