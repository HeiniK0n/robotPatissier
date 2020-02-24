

class CoupleRedditeurPotCom: # Définition de notre classe 
    """Classe définissant une personne caractérisée par :
    - son redditeur
    - son poteau ou commentaire
    """

    
    def __init__(self,redditeur,potCom): # Notre méthode constructeur
        """Pour l'instant, on ne va définir qu'un seul attribut"""
        self.redditeur = redditeur
        self.potCom=potCom