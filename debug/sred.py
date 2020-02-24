
from threading import Thread, RLock
from time import sleep

# verou = RLock()
class Multi(Thread):
    
    def __init__(self, tablo,name):
        Thread.__init__(self)
        self.name = name
        self.tablo =tablo

    def run(self):
        
        for val in self.tablo :
            atester = val *2

            if atester not in resultat :
                resultat.append(atester)
                sleep(1)
                print(self.name +" -> " + str(atester) + " a rajouter ") 
                
            else : 
                print(self.name +" -> " + str(atester) + " deja present") 
        
        print(self.name,resultat)

if __name__ == "__main__":
    
    global resultat
    
    resultat = [6]
    
    
    
    tablo1 =[2,4,6,8,3,3,5,14,9,11,13,10,12,14]
    
    tablo2 =[4,7,3,3,5,14,9,11,13,3,3,5,14,9,11,13,3,3,5,14,9,11,13,3,3,5,14,9,11,13,3,3,5,14,9,11,13,3,3,5,14,9,11,13]
    
    
    thread1 = Multi(tablo1,"thread 1")
    thread2 = Multi(tablo2,"    thread 2")

    
    
    
    thread1.start()
    thread2.start()

   
    
    