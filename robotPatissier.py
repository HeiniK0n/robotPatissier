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
    poteauOuCommentaire.reply(JoyeuxJourDuGateauTexte)

#  ============================    

def sauvegardeListeDesMangeursDeGateaux(listeRedditeurDejaFourniEnGateau):
    with open(leFichierDesLaureats, 'w') as f:
        for item in listeRedditeurDejaFourniEnGateau:
            f.write("%s\n" % item)
    f.close()

#  ============================    

def estCeLeJourDuGateaux ( moisTest , jourTest, redditeur,poteauOuCommentaire):
#     moisActuel=3 #pour debug
#     jourActuel=5 #pour debug
    if redditeur in listeRedditeurDejaFourniEnGateau :
        print(redditeur +" déjà gateauisé")
    else :
        if int(moisTest) == int(moisActuel) :
            if int(jourTest) == int(jourActuel) :
                print(" jour du gateau pour "+redditeur)
                souhaiterJourDuGateau(poteauOuCommentaire, redditeur)
                
                listeRedditeurDejaFourniEnGateau.append(redditeur)

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
            if j > 10 :
                break
            
        if i > 10:
            break
    sauvegardeListeDesMangeursDeGateaux(listeRedditeurDejaFourniEnGateau)  

#  ============================    

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        logging.warning("Usage: `python robotPatisier.py identifiants`   ou identifiants est un fichier de type `\n nombot \n client_id:client_secret \n username:password`")
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
    except:
        logging.warning("Fichier 'identifiants' invalide.")
        logging.warning("Usage: `./robotPatisier identifiants`   ou identifiants est un fichier de type `\n nombot \n client_id:client_secret \n username:password`")
        sys.exit(-1)
        
    if "nom" not in ID or "client_id" not in ID or "client_secret" not in ID or "username" not in ID or "password" not in ID:
        logging.warning("Fichier 'identifiants' invalide.")
        sys.exit(-1)

    today = date.today()
    
    global leFichierDesLaureats
    
    listeRedditeurDejaFourniEnGateau = []
    
    leFichierDesLaureats = "laureatsDuJour.txt"
    
    if dt.datetime.fromtimestamp(os.path.getctime(leFichierDesLaureats)).date() == today:
        print('fichier du jour')
        fichier = open(leFichierDesLaureats,'r+') 
        for line in fichier : 
            print(line)
            if (len(line.strip())> 0 ) :
                listeRedditeurDejaFourniEnGateau.append(line.strip())
    else :
        print('fichier ancien a vider')
        fichier = open(leFichierDesLaureats,'w') 
    
    if len(listeRedditeurDejaFourniEnGateau) > 0 :
        print(" Ils ont déjà eu le gateau : ")
        print( listeRedditeurDejaFourniEnGateau)
    
    
    global jourActuel, moisActuel
    jourActuel = today.strftime("%d")
    moisActuel = today.strftime("%m")
    print("On est le  =", jourActuel +"/"+ moisActuel)

    luceci = praw.Reddit(user_agent=ID["nom"],
                         client_id=ID["client_id"],
                         client_secret=ID["client_secret"],
                         username=ID["username"],
                         password=ID["password"])

    
    sousmarin = luceci.subreddit('rance').new()

    Thread(target = listerPoteaux, args=(sousmarin,)).start()
    
    

