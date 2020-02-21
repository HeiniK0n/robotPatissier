# coding: utf8
#!/usr/bin/env python3
'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from datetime import date
from datetime import datetime
import datetime as dt
from threading import Thread
import praw
import os.path
import logging
import sys
import emoji
import time
 


def souhaiterJourDuGateau(poteauOuCommentaire,redditeur):
    JoyeuxJourDuGateauTexte  = "Joyeux jour du gateau [u/"+redditeur[:redditeur.index('[')]+"](https://www.reddit.com/user/"+redditeur[:redditeur.index('[')]+")" 
    #JoyeuxJourDuGateauTexte +="\n\n biipe  ! Tiens 🍰 !  bipe bipe ! (style rançais) \n\n---\n\n" 
    if ID['sousmarin'] == "rance" :
        JoyeuxJourDuGateauTexte +="\n\n biipe  ! Tiens " + emoji.emojize(':shortcake:') + " !  bipe bipe ! (style rançais) \n\n---\n\n" 
    else :
        JoyeuxJourDuGateauTexte +="\n\n beeep  ! Tiens " + emoji.emojize(':shortcake:') + " !  beep beep !  \n\n---\n\n"
    JoyeuxJourDuGateauTexte += "^( Je suis )[u/LeReauBeau](https://www.reddit.com/user/LeReauBeau) ^(ton Robot Patissier Personnel ! Profite ! Régale-toi ! )"
    print(JoyeuxJourDuGateauTexte)
    poteauOuCommentaire.reply(JoyeuxJourDuGateauTexte)

#  ============================    

def sauvegardeListeDesMangeursDeGateaux(listeRedditeursDejaFournisEnGateaux):
    with open(leFichierDesLaureats, 'w') as f:
        for item in listeRedditeursDejaFournisEnGateaux:
            f.write("%s\n" % item)
    f.close()
    print(" \n Sauvegarde des bouffeurs de gateaux et AUREVOIR")
    if len(listeRedditeursDejaFournisEnGateaux) > 0 :
        print(" \n les gateauisés du jour : ")
        print( listeRedditeursDejaFournisEnGateaux)

#  ============================    

def estCeLeJourDuGateaux ( moisTest , jourTest, redditeur, poteauOuCommentaire):
#     moisTest=2 #pour debug
#     jourTest=18 #pour debug
    if redditeur in listeRedditeursDejaFournisEnGateaux :
        print(redditeur +" déjà gateauisé")
    else :
        if int(moisTest) == int(moisActuel) :
            if int(jourTest) == int(jourActuel) :
                print(" jour du gateau pour "+redditeur)
                souhaiterJourDuGateau(poteauOuCommentaire, redditeur)
                
                listeRedditeursDejaFournisEnGateaux.append(redditeur)

#  ============================        

def listerCommentaires(listeCommentaires, profondeur):
     for j,commentaire in enumerate(listeCommentaires) :
        try : 
            if  commentaire.author is not None :
                dt_objectCommentaire = datetime.fromtimestamp(commentaire.created_utc)
                
                if str(dt_objectCommentaire.day) == jourActuel or len(commentaire.replies)>0 :
                
                    dt_objectRedditeurCommenteur = datetime.fromtimestamp(commentaire.author.created)
                    print("\t"+ profondeur+" Commenteur = "+commentaire.author.name + "[" + commentaire.author.id + "] " 
                          + str(dt_objectRedditeurCommenteur.day) + "/" 
                          + str(dt_objectRedditeurCommenteur.month) + "/"
                          + str(dt_objectRedditeurCommenteur.year)  + " => commentaire = ["
                          + str(dt_objectCommentaire.day) + "/"
                          + str(dt_objectCommentaire.month) + "/"
                          + str(dt_objectCommentaire.year) + "]")
        
                    if   str(dt_objectRedditeurCommenteur.year) != anneeActuelle  :
                        estCeLeJourDuGateaux (dt_objectRedditeurCommenteur.month , dt_objectRedditeurCommenteur.day, commentaire.author.name + "[" + commentaire.author.id + "]" , commentaire)
                    
                    if len(commentaire.replies)>0 :
                        listerCommentaires(commentaire.replies,profondeur +"\t")
        except :
            print("erreur sur commentaire : "+str(commentaire.id) +  " , num :"+ str(j))
        finally :                 
            if j >= int(ID["profondeurCommentaire"]):
                break
    
#  ============================        

def listerPoteaux(sousmarin):
    '''Thread qui espionne les poteaux'''
    for i, poteau in enumerate(sousmarin):
        try :
            if i==14 : 
                print ("debug")
            dt_objectPoteau = datetime.fromtimestamp(poteau.created_utc)
            print("\n ------------\n "+str(i)+ " " + poteau.title 
                  + "[" + str(dt_objectPoteau.day)
                  + "/" + str(dt_objectPoteau.month)
                  + "/" + str(dt_objectPoteau.year) + "]")
            
            dt_objectAuteur = datetime.fromtimestamp(poteau.author.created)
            print("\t Auteur  = " + poteau.author.name + "[" + poteau.author.id + "] " 
                  + str(dt_objectAuteur.day) + "/" 
                  + str(dt_objectAuteur.month) + "/"
                  + str(dt_objectAuteur.year) )
            
            if (str(dt_objectAuteur.year) != anneeActuelle and dt_objectPoteau.day == jourActuel) :
                estCeLeJourDuGateaux (str(dt_objectAuteur.month), str(dt_objectAuteur.day), poteau.author.name + "[" + poteau.author.id + "]" , poteau)
            
            if len(poteau.comments)>0 :
                listerCommentaires(poteau.comments, "\t")
        except :
            print("erreur sur poteau : "+str(poteau.id) +  " , num :"+ str(i))
        finally:        
            if i >= int(ID["profondeurPoteau"]):
                break
        
    sauvegardeListeDesMangeursDeGateaux(listeRedditeursDejaFournisEnGateaux)  

#  ============================    

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        logging.warning("Usage: `./robotPatisier parametres` "  
        + " ou parametres est un fichier de type "
        + " `\n nombot "
        + " \n client_id:client_secret "
        + " \n username:password "
        + " \n profondeurPoteau:profondeurCommentaire "
        + " \n sousmarin`")
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
                    ID["sousmarin"] = elem[0]
    except:
        logging.warning("Fichier 'parametres' invalide.")
        logging.warning("Usage: `./robotPatisier parametres` "  
        + " ou parametres est un fichier de type "
        + " `\n nombot "
        + " \n client_id:client_secret "
        + " \n username:password "
        + " \n profondeurPoteau:profondeurCommentaire "
        + " \n sousmarin`")
        sys.exit(-1)
        
    today = date.today()
    
    global leFichierDesLaureats
    
    listeRedditeursDejaFournisEnGateaux = []
    
    leFichierDesLaureats = "laureatsDuJour.txt"
	
    print("===============================================\n===============================================")    
    print(time.strftime("%Y-%m-%d %H:%M"))
    print(ID["sousmarin"])
    print("===============================================\n===============================================")    

    if dt.datetime.fromtimestamp(os.path.getctime(leFichierDesLaureats)).date() == today:
        print('fichier du jour')
        fichier = open(leFichierDesLaureats,'r+') 
        for line in fichier : 
            print(line)
            if (len(line.strip())> 0 ) :
                listeRedditeursDejaFournisEnGateaux.append(line.strip())
    else :
        print('fichier ancien a vider')
        fichier = open(leFichierDesLaureats,'w') 
    
    if len(listeRedditeursDejaFournisEnGateaux) > 0 :
        print(" Ils ont déjà eu le gateau : ")
        print( listeRedditeursDejaFournisEnGateaux)
    
    
    global jourActuel, moisActuel, anneeActuelle
    jourActuel = today.strftime("%d")
    moisActuel = today.strftime("%m")
    anneeActuelle = today.strftime("%Y")
    print("On est le  =", jourActuel +"/"+ moisActuel +"/"+ anneeActuelle)

    luceci = praw.Reddit(user_agent=ID["nom"],
                         client_id=ID["client_id"],
                         client_secret=ID["client_secret"],
                         username=ID["username"],
                         password=ID["password"])
    
    sousmarin = luceci.subreddit(ID["sousmarin"]).new()
    print("--------------------------------------------------------------------------", datetime.now())
#     Thread(target = listerPoteaux, args=(sousmarin,)).start()
    listerPoteaux(sousmarin)
    print("--------------------------------------------------------------------------", datetime.now())
