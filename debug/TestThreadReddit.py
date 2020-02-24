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

def souhaiterJourDuGateau(poteauOuCommentaire,redditeur):

    leSous=poteauOuCommentaire.subreddit.display_name

    if leSous=='funny' :
        JoyeuxJourDuGateauTexte="Happy cake day [u/"+redditeur[:redditeur.index('[')]+"](https://www.reddit.com/user/"+redditeur[:redditeur.index('[')]+")" 
    else :    
        JoyeuxJourDuGateauTexte  = "Joyeux jour du gateau [u/"+redditeur[:redditeur.index('[')]+"](https://www.reddit.com/user/"+redditeur[:redditeur.index('[')]+")" 

    if leSous=='funny' :
        JoyeuxJourDuGateauTexte +="\n\n beeep  ! Take it " + emoji.emojize(':shortcake:') + " !  beep beep !  \n\n---\n\n"
    else :
        if leSous == "rance" :
            JoyeuxJourDuGateauTexte +="\n\n biipe  ! Tiens " + emoji.emojize(':shortcake:') + " !  bipe bipe ! (style rançais) \n\n---\n\n" 
        else :
            JoyeuxJourDuGateauTexte +="\n\n beeep  ! Tiens " + emoji.emojize(':shortcake:') + " !  beep beep !  \n\n---\n\n"

    if leSous=='funny' :        
        JoyeuxJourDuGateauTexte += "^( I am )[u/LeReauBeau](https://www.reddit.com/user/LeReauBeau) ^(your personnal pastry cooking Bot ! Enjoy ! Bon appetit )"
    else :
        JoyeuxJourDuGateauTexte += "^( Je suis )[u/LeReauBeau](https://www.reddit.com/user/LeReauBeau) ^(ton Robot Patissier Personnel ! Profite ! Régale-toi ! )"

    try :   
        poteauOuCommentaire.reply(JoyeuxJourDuGateauTexte)
        print(JoyeuxJourDuGateauTexte + "\n")
    except Exception as erreur:
        raise erreur

#  ============================

def sauvegardeListeDesMangeursDeGateaux(listeRedditeursDejaFournisEnGateaux):

    with open(leFichierDesLaureats, 'w') as f:
        for item in listeRedditeursDejaFournisEnGateaux:
            f.write("%s\n" % item)
    f.close()
    print("- Sauvegarde des bouffeurs de gateaux")
    if len(listeRedditeursDejaFournisEnGateaux) > 0 :
        print("- Les 'gateauisés' du jour : ")
        print( listeRedditeursDejaFournisEnGateaux)

#  ============================

def estCeLeJourDuGateaux ( moisTest , jourTest, redditeur, poteauOuCommentaire):

    threadLock.acquire() # Get lock to synchronize threads
    if redditeur in listeRedditeursDejaFournisEnGateaux :
        print("\n *** "+redditeur +" déjà gateauisé ***\n")
    else :
        if int(moisTest) == int(moisActuel) :
            if int(jourTest) == int(jourActuel) :
                print("\n *** Jour du gateau pour "+redditeur+ " ***\n")

                try :
                    souhaiterJourDuGateau(poteauOuCommentaire, redditeur)
                    listeRedditeursDejaFournisEnGateaux.append(redditeur)
                except Exception as erreur:
                    print ('- ERREUR sur le souhaitage... ', erreur)
    threadLock.release()# Free lock to release next thread

#  ============================

def listerCommentaires(listeCommentaires,filVarPrint,profondeur):

    profondeur=profondeur+"\t"
    for j,commentaire in enumerate(listeCommentaires) :
        try : 
            if  commentaire.author is not None :

                dt_objectCommentaire = datetime.fromtimestamp(commentaire.created_utc)

                if str(dt_objectCommentaire.day) == jourActuel or len(commentaire.replies)>0 :

                    dt_objectRedditeurCommenteur = datetime.fromtimestamp(commentaire.author.created_utc)

                    print( filVarPrint + "/"+ str(commentaire.id)+"] Commenteur "+str(j+1)+" = "+commentaire.author.name + "[" + commentaire.author.id + "] " 
                          + str(dt_objectRedditeurCommenteur.day) + "/" 
                          + str(dt_objectRedditeurCommenteur.month) + "/"
                          + str(dt_objectRedditeurCommenteur.year)  + " => commentaire = ["
                          + str(dt_objectCommentaire.day) + "/"
                          + str(dt_objectCommentaire.month) + "/"
                          + str(dt_objectCommentaire.year) + "]")

                if str(dt_objectRedditeurCommenteur.year) != anneeActuelle  :
                    estCeLeJourDuGateaux (dt_objectRedditeurCommenteur.month , dt_objectRedditeurCommenteur.day, commentaire.author.name + "[" + commentaire.author.id + "]" , commentaire)

                if len(commentaire.replies)>0 :
                    listerCommentaires(commentaire.replies,filVarPrint + "/" + str(commentaire.id),profondeur+"\t")
        except Exception as erreur :
            print("- ERREUR sur commentaire : "+str(commentaire.id) +  " , num :"+ str(j+1) + " -> "+str(erreur))
        finally :                 
            if j >= int(ID["profondeurCommentaire"]):
                break

#  ============================

def listerPoteaux(poteauxDuSousmarin,unNomDeSous):

        for i, poteau in enumerate(poteauxDuSousmarin):
            try :
                dt_objectPoteau = datetime.fromtimestamp(poteau.created_utc)

                varPrint= str(i+1)+"["+ unNomDeSous + "/"+ str(poteau.id)
                print(varPrint +"] Poteau = " + poteau.title 
                      + "[" + str(dt_objectPoteau.day)
                      + "/" + str(dt_objectPoteau.month)
                      + "/" + str(dt_objectPoteau.year) + "]")

                dt_objectAuteur = datetime.fromtimestamp(poteau.author.created_utc)

                print( varPrint +"] Auteur = " + poteau.author.name + "[" + poteau.author.id + "] " 
                      + str(dt_objectAuteur.day) + "/" 
                      + str(dt_objectAuteur.month) + "/"
                      + str(dt_objectAuteur.year) )

                if (str(dt_objectAuteur.year) != anneeActuelle and str(dt_objectPoteau.day) == jourActuel) :
                    estCeLeJourDuGateaux (str(dt_objectAuteur.month), str(dt_objectAuteur.day), poteau.author.name + "[" + poteau.author.id + "]" , poteau)

                if len(poteau.comments)>0 :
                    listerCommentaires(poteau.comments,varPrint, "\t")

            except Exception as erreur :
                print("- ERREUR sur poteau : "+str(poteau.id) +  " , num :"+ str(i) + " -> "+str(erreur))

#  ============================

class ParcoureurDePoteaux(Thread):

    def __init__(self, poteauxDuSousmarin,unNomDeSous):
        Thread.__init__(self)
        self.unNomDeSous = unNomDeSous
        self.poteauxDuSousmarin =poteauxDuSousmarin

    def run(self):
        listerPoteaux(self.poteauxDuSousmarin,self.unNomDeSous)

#  ============================

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: `./robotPatisier parametres` "  
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
        print("Usage: `./robotPatisier parametres` "  
        + " ou parametres est un fichier de type "
        + " `\n nombot "
        + " \n client_id:client_secret "
        + " \n username:password "
        + " \n profondeurPoteau:profondeurCommentaire "
        + " \n sousmarins(séparés par des tirets) "
        + " \n nom du fichier de sauvegarde des gateauisés du jour`")
        sys.exit(-1)

    today = date.today()

    global leFichierDesLaureats

    listeRedditeursDejaFournisEnGateaux = []

    leFichierDesLaureats = ID["NomDuFichierDeSauvegarde"]

    start_time = time.time() 
    print("===============================\n= start : "+time.strftime("%Y-%m-%d %H:%M:%S")+" =\n===============================")        

    try :
        os.path.getctime(leFichierDesLaureats)
    except :
        fichier = open(leFichierDesLaureats, 'w+')
        fichier.close()

    if dt.datetime.fromtimestamp(os.path.getctime(leFichierDesLaureats)).date() == today:
        print('- Fichier du jour : '+str(leFichierDesLaureats))
        fichier = open(leFichierDesLaureats,'r+') 
        for line in fichier : 
            print(line)
            if (len(line.strip())> 0 ) :
                listeRedditeursDejaFournisEnGateaux.append(line.strip())
    else :
        print('- Fichier ancien a vider')
        fichier = open(leFichierDesLaureats,'w') 

    if len(listeRedditeursDejaFournisEnGateaux) > 0 :
        print("- Ils ont déjà eu leur part du gateau : ")
        print( listeRedditeursDejaFournisEnGateaux)

    print("=============================")

    global jourActuel, moisActuel, anneeActuelle
    jourActuel = today.strftime("%d")
    moisActuel = today.strftime("%m")
    anneeActuelle = today.strftime("%Y")

    luceci = praw.Reddit(user_agent=ID["nom"],
                         client_id=ID["client_id"],
                         client_secret=ID["client_secret"],
                         username=ID["username"],
                         password=ID["password"])

#     print( datetime.fromtimestamp((luceci.redditor("Le_Utinam").created_utc)).strftime("%Y-%m-%d") )
#     print( datetime.fromtimestamp((luceci.redditor("Magical__Fetus").created_utc)).strftime("%Y-%m-%d") )
     

    threadLock = threading.Lock()
    threads = []

    for unNomDeSous in ID["sousmarins"].strip().split('-'):        
        poteauxDuSousmarin = luceci.subreddit(unNomDeSous).new(limit=int(ID["profondeurPoteau"]))
        threadParcoureur = ParcoureurDePoteaux(poteauxDuSousmarin,unNomDeSous)
        threadParcoureur.start()
        threads.append(threadParcoureur)

    for t in threads :
        t.join()   

    print("=============================")    
    sauvegardeListeDesMangeursDeGateaux(listeRedditeursDejaFournisEnGateaux)  

    print("=============================\n= end : "+time.strftime("%Y-%m-%d %H:%M:%S")+" =\n=============================")
    print("Temps d execution : ",  time.strftime('%H:%M:%S', time.gmtime((time.time() - start_time))))

    print("======== AUREVOIR ===========")  
