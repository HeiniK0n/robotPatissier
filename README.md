# robotPatissier
Fournisseur de jour du gateau pour Reddit (sousmarin r/rance) 
Reddit happy cakeday provider (sub r/rance)

=========================  
First , create a reddit account https://www.reddit.com/register/?dest=https%3A%2F%2Fwww.reddit.com%2F  

It will give you a username an a password

Then create a reddit application script type  there : https://www.reddit.com/prefs/apps  

It will setup an client_id and client_secret 

These 4 informations will be mandatory in 'identifiants' file

=========================  
Then launch the main script with the 'identifiants' file as argument.

```
python robotPatissier.py identifiants
```

---
Actually, it is targeted for teh sub r/rance on the 10 last new posts, of course you can change the sub targeted, and the numbers of post scanned

I know it can easily improved.
