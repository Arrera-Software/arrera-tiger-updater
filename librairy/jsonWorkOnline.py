import json
import requests

class jsonWorkOnline :
    def __init__(self):
        self.fichier = str 
        self.contenuJson = str
        self.__onlineFile = bool
        self.__localFile = bool
    
    def __reloadFile(self):
        if ((self.__localFile==True) and (self.__onlineFile==False)):
            self.__readFile.close()
            self.__readFile = open(self.fichier, 'r', encoding='utf-8')
            self.__readFile.seek(0)  # Rembobiner le fichier au début
            self.contenuJson = json.load(self.__readFile)
        
    def loadFile(self, fichier: str):
        self.fichier = fichier
        self.__readFile =  open(fichier, 'r', encoding='utf-8') 
        self.contenuJson = json.load(self.__readFile)
        self.__localFile=True
        self.__onlineFile=False
    
    def loadInternet(self,url:str):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.contenuJson = response.json()
            self.__localFile=False
            self.__onlineFile=True
        except requests.exceptions.RequestException as e:
            self.__localFile=False
            self.__onlineFile=False
        
    def lectureJSON(self,flag): # Permet de lire la valeur du flag defini a l'appel de la fonction
        if ((self.__localFile==True) or (self.__onlineFile==True)):
            dict = self.contenuJson[flag]
            return str(dict)
        else :
            return "error"
    
    def lectureJSONMultiFlag(self,flag1,flag2):
        if ((self.__localFile==True) or (self.__onlineFile==True)):
            dict = self.contenuJson[flag1][flag2]
            return str(dict)
        else :
            return "error"
    
    def lectureJSONList(self,flag):
        if ((self.__localFile==True) or (self.__onlineFile==True)):
            liste = self.contenuJson[flag]
            return list(liste)
        else :
            return ["aaaa","aaa"]
    
    def lectureJSONDict(self,flag):
        if ((self.__localFile==True) or (self.__onlineFile==True)):
            dictionnaire = self.contenuJson[flag]
            return dict(dictionnaire)
        else :
            return {"aaaaa":"aaaa","aaaaa":"aaaa","aaaaa":"aaaa"} 



    def dictJson(self):
        return self.contenuJson
       
    def compteurFlagJSON(self):
        return len(self.contenuJson)