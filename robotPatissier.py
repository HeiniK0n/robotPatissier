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
 


def souhaiterJourDuGateau(poteauOuCommentaire,redditeur):
    JoyeuxJourDuGateauTexte = "Joyeux jour du gateau " +redditeur[:redditeur.index('[')]
    JoyeuxJourDuGateauTexte+="\n\n bipe bipe  ! Tiens 🍰  bipe bipe ! (à la rançaise) \n\n---\n\n" 
    JoyeuxJourDuGateauTexte+= "^( Je suis ton Robot Patissier Personnel ! \n\n" + " Profites ! Gourmand !)^"
    print(JoyeuxJourDuGateauTexte)
#     poteauOuCommentaire.reply(JoyeuxJourDuGateauTexte)

#  ============================    

def sauvegardeListeDesMangeursDeGateaux(listeRedditeursDejaFournisEnGateaux):
    with open(leFichierDesLaureats, 'w') as f:
        for item in listeRedditeursDejaFournisEnGateaux:
            f.write("%s\n" % item)
    f.close()
    print(" Sauvegarde des bouffeurs de gateaux et AUREVOIR")

#  ============================    

def estCeLeJourDuGateaux ( moisTest , jourTest, redditeur,poteauOuCommentaire):
#     moisActuel=3 #pour debug
#     jourActuel=5 #pour debug
    if redditeur in listeRedditeursDejaFournisEnGateaux :
        print(redditeur +" déjà gateauisé")
    else :
        if int(moisTest) == int(moisActuel) :
            if int(jourTest) == int(jourActuel) :
                print(" jour du gateau pour "+redditeur)
                souhaiterJourDuGateau(poteauOuCommentaire, redditeur)
                
                listeRedditeursDejaFournisEnGateaux.append(redditeur)

#  ============================        

def listerPoteaux(sousmarin):
    '''Thread qui espionne les poteaux'''
    for i, poteau in enumerate(sousmarin):
        print("\n ------------\n" + poteau.title)
        dt_object = datetime.fromtimestamp(poteau.author.created)
        jourRedditeurAuteur = str(dt_object.day)
        moisRedditeurAuteur = str(dt_object.month)
        print("\t Auteur  = " + poteau.author.name + "[" + poteau.author.id + "] " + jourRedditeurAuteur + "/" + moisRedditeurAuteur)
        estCeLeJourDuGateaux (moisRedditeurAuteur , jourRedditeurAuteur, poteau.author.name + "[" + poteau.author.id + "]" , poteau)
        
        for j,commentaire in enumerate(poteau.comments) :
            dt_object = datetime.fromtimestamp(commentaire.author.created)
            #print("dt_object =", dt_object)
            jourRedditeurCommenteur = str(dt_object.day)
            moisRedditeurCommenteur = str(dt_object.month)
            print("\t Commenteur = "+commentaire.author.name + "[" + commentaire.author.id + "] " + jourRedditeurCommenteur + "/" + moisRedditeurCommenteur)
            estCeLeJourDuGateaux (moisRedditeurCommenteur , jourRedditeurCommenteur, commentaire.author.name + "[" + commentaire.author.id + "]" , commentaire)
            if j > int(ID["profondeurCommentaire"]):
                break
            
        if i > int(ID["profondeurPoteau"]):
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
        
    if "nom" not in ID or "client_id" not in ID or "client_secret" not in ID or "username" not in ID or "password" not in ID:
        logging.warning("Fichier 'parametres' invalide.")
        sys.exit(-1)

    today = date.today()
    
    global leFichierDesLaureats
    
    listeRedditeursDejaFournisEnGateaux = []
    
    leFichierDesLaureats = "laureatsDuJour.txt"
    
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
    
    
    global jourActuel, moisActuel
    jourActuel = today.strftime("%d")
    moisActuel = today.strftime("%m")
    print("On est le  =", jourActuel +"/"+ moisActuel)

    luceci = praw.Reddit(user_agent=ID["nom"],
                         client_id=ID["client_id"],
                         client_secret=ID["client_secret"],
                         username=ID["username"],
                         password=ID["password"])

    
    sousmarin = luceci.subreddit(ID["sousmarin"]).new()

    Thread(target = listerPoteaux, args=(sousmarin,)).start()
    
    

