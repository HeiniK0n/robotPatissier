# 
# import datetime
# import time
# 
# # Debut du decompte du temps
# start_time = time.time() 
#  
#  
#  
# time.sleep(5)
#  
# # Affichage du temps d execution
# print("Temps d execution : ",  time.strftime('%H:%M:%S', time.gmtime((time.time() - start_time))))
import emoji
redditeur='totolariflette[rr'
leSous='ferance'
SOUS_FRANCOPHONE={'france','rance'}

if leSous in SOUS_FRANCOPHONE :
    JoyeuxJourDuGateauTexte  = "Joyeux jour du gateau [u/"+redditeur[:redditeur.index('[')]+"](https://www.reddit.com/user/"+redditeur[:redditeur.index('[')]+")" 
    if leSous == "rance" :
        JoyeuxJourDuGateauTexte +="\n\n biipe  ! Tiens " + emoji.emojize(':shortcake:') + " !  bipe bipe ! (style rançais) \n\n---\n\n" 
    else :
        JoyeuxJourDuGateauTexte +="\n\n beeep  ! Tiens " + emoji.emojize(':shortcake:') + " !  beep beep !  \n\n---\n\n"
    JoyeuxJourDuGateauTexte += "^( Je suis )[u/LeReauBeau](https://www.reddit.com/user/LeReauBeau) ^(ton Robot Patissier Personnel ! Profite ! Régale-toi ! )"
else :    
    JoyeuxJourDuGateauTexte="Happy cake day [u/"+redditeur[:redditeur.index('[')]+"](https://www.reddit.com/user/"+redditeur[:redditeur.index('[')]+")" 
    JoyeuxJourDuGateauTexte +="\n\n beeep  ! Take it " + emoji.emojize(':shortcake:') + " !  beep beep !  \n\n---\n\n"
    JoyeuxJourDuGateauTexte += "^( I am )[u/LeReauBeau](https://www.reddit.com/user/LeReauBeau) ^(your personnal pastry cooking Bot ! Enjoy ! Bon appetit )"

print(JoyeuxJourDuGateauTexte + "\n")