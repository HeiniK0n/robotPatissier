# robotPatissier 


Fournisseur de jour du gateau pour Reddit 

Reddit happy cakeday provider 

The purpose is to comment the post or the comments with a 'happy cake day' quote for the user that the cake day is reached today.

It scan the post author 's account creation date or any commentator's account creation date, 

and if it's today then it comment "Joyeux jour du gateau"  
This script must run several times a day to avoid missing any cake day. (check cron)

=========================  
1. First , create a reddit account https://www.reddit.com/register/?dest=https%3A%2F%2Fwww.reddit.com%2F  

	It will give you a username an a password.

2. Then create a reddit application script type  there : https://www.reddit.com/prefs/apps  

	It will setup an client_id and client_secret.

3. Then set up the numbers of posts scanned and also the numbers of comments scanned.

4. Finally, set up the sub targeted.

All these informations will be mandatory in 'parametres' file.

=========================  
Then launch the main script with the 'parametres' file as argument.

```
python robotPatissier.py parametres
```

There is some rules to keep in mind :  
- You need python3  
- you have to install python modules with pip :  praw and emoji  
```
pip install -r requirements.txt
```


PS :(maybe I will explain all the environment sh.t I've been through...)


---



I know it can easily improved. Have fun.
