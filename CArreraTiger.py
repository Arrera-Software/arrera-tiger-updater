from librairy.jsonWorkOnline import*
from librairy.travailJSON import*
import urllib.request
from librairy.dectectionOS import*
import zipfile
import os
from pathlib import Path
import shutil


class CArreraTiger :
    def __init__(self,tigerFile:str):
        # Initialisation des attributs
        self.__url = ""
        self.__emplacementSoft = ""
        # Initialisation de l'objet pour lire le depot
        self.__depotFile = jsonWorkOnline()
        # Chargement du fichier local
        self.__tigerFile = jsonWork(tigerFile)
        # Initialisation de l'objet pour la detection du systeme d'explotation
        self.__system = OS()

    def loadDepots(self,url:str):
        if url == "":
            return False
        else :
            self.__url = url
            self.__depotFile.loadInternet(url)
            return True

    def loadEmplacementFile(self):
        folder = self.__tigerFile.lectureJSON("folder")
        if folder == "":
            return False
        else :
            self.__emplacementSoft = folder
            return True

    def setEmplacementArreraSoft(self,emplacementSoft : str):
        if emplacementSoft == "":
            return False
        else :
            self.__emplacementSoft = emplacementSoft
            self.__tigerFile.EcritureJSON("folder",self.__emplacementSoft)
            return True

    def getEmplacementSaved(self):
        if not self.__emplacementSoft :
            return False
        else :
            return True

    def checkUpdate(self):
        softInstalled = self.getSoftInstall()

        if softInstalled[0] == "Aucun logiciel installé":
            return []
        else :
            osLinux = self.__system.osLinux()
            osWindows = self.__system.osWindows()
            listOut = []
            dictSoft = self.__depotFile.dictJson()

            for i in range(0,len(softInstalled)):
                if (osLinux == True):
                   directorySoft = self.__emplacementSoft+"/"+dictSoft[softInstalled[i]]["namefolderLinux"]
                else :
                    if (osWindows == True):
                        directorySoft = self.__emplacementSoft+"/"+dictSoft[softInstalled[i]]["namefolderWin"]
                    else :
                        return []

                if os.path.exists(directorySoft):
                    versionInstalled = ""
                    with open(directorySoft+"/VERSION", "r") as fichier:
                        for ligne in fichier:
                            # Si la ligne commence par "VERSION="
                            if ligne.startswith("VERSION="):
                                # Supprimer le saut de ligne éventuel et récupérer la valeur
                                version = ligne.strip().split("=")[1]
                                versionInstalled = version
                        fichier.close()

                    if (versionInstalled != "IXXXX-XXX"):
                        versionOnline = dictSoft[softInstalled[i]]["version"]
                        if (versionInstalled != versionOnline):
                            listOut.append(softInstalled[i])
                else :
                    return []

            return  listOut



    def update(self, soft: str):
        softUpdated = self.checkUpdate()

        if soft not in softUpdated:
            return False

        dictSofts = self.__depotFile.dictJson()
        dictSoft = dictSofts[soft]
        osLinux = self.__system.osLinux()
        osWindows = self.__system.osWindows()

        listFileNoSuppr = dictSoft["listFileUser"] + ["VERSION"]
        directorySoft = ""
        if osLinux:
            listFileNoSuppr.append("lauch.sh")
            directorySoft = self.__emplacementSoft + "/" + dictSoft['namefolderLinux']
        elif osWindows:
            directorySoft = self.__emplacementSoft + "/" + dictSoft['namefolderWin']
        else:
            return False

        for root, _, files in os.walk(directorySoft):
            for file in files:
                if file not in listFileNoSuppr:
                    os.remove(os.path.join(root, file))

        for root, dirs, files in os.walk(directorySoft, topdown=False):
            for file in files:
                if file not in listFileNoSuppr:
                    os.remove(os.path.join(root, file))
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)

        if osLinux == True :
            link = dictSoft["linkLinux"]
            fileName = "tmp/" + dictSoft["nameziplinux"]
        else:
            if osWindows == True :
                link = dictSoft["linkWin"]
                fileName = "tmp\\" + dictSoft["namezipwin"]
            else:
                return False

        if not link:
            return False

        urllib.request.urlretrieve(link, fileName)
        if not os.path.exists(fileName):
            return False
        if not os.path.exists("tmp/"):
            os.makedirs("tmp/")
        with zipfile.ZipFile(fileName, 'r') as zip_ref:
            zip_ref.extractall("tmp/")

        if osLinux == True:
            for root, _, files in os.walk("tmp/" + dictSoft["namefolderLinux"]):
                for file in files:
                    if file not in listFileNoSuppr:
                        src_file = os.path.join(root, file)
                        dest_file = os.path.join(directorySoft, os.path.relpath(src_file, "tmp/" + dictSoft["namefolderLinux"]))
                        dest_dir = os.path.dirname(dest_file)
                        if not os.path.exists(dest_dir):
                            os.makedirs(dest_dir)
                        shutil.copy2(src_file, dest_file)
        else :
            if osWindows == True :
                for root, _, files in os.walk("tmp\\" + dictSoft["namefolderWin"]):
                    for file in files:
                        if file not in listFileNoSuppr:
                            src_file = os.path.join(root, file)
                            dest_file = os.path.join(directorySoft, os.path.relpath(src_file, "tmp\\" + dictSoft["namefolderWin"]))
                            dest_dir = os.path.dirname(dest_file)
                            if not os.path.exists(dest_dir):
                                os.makedirs(dest_dir)
                            shutil.copy2(src_file, dest_file)
            else :
                return  False

        with open(f"{directorySoft}/VERSION", "w") as file:
            file.write("VERSION=" + dictSoft["version"] + "\n")
            file.write("NAME=" + soft.upper())

        for filename in os.listdir("tmp/"):
            file_path = os.path.join("tmp/", filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        return True

    def install(self, soft : str):
        softInstalled = self.getSoftInstall()
        softAvailable = self.getSoftAvailable()

        if (soft in softInstalled):
            return False
        else :
            if soft not in softAvailable :
                return False
            else:
                linuxOs = self.__system.osLinux()
                windowsOS = self.__system.osWindows()
                dictSofts = self.__depotFile.dictJson()
                dictSoft = dictSofts[soft]
                if (windowsOS == True):
                    link = dictSoft["linkWin"]
                    fileName = self.__emplacementSoft+"/"+dictSoft["namezipwin"]
                else :
                    if (linuxOs == True):
                        link = dictSoft["linkLinux"]
                        fileName = self.__emplacementSoft+dictSoft["nameziplinux"]
                    else :
                        return False

                if (link == ""):
                    return False
                else :
                    urllib.request.urlretrieve(link,fileName)
                    if not os.path.exists(fileName):
                        return False
                    if not os.path.exists(self.__emplacementSoft):
                        os.makedirs(self.__emplacementSoft)
                    with zipfile.ZipFile(fileName, 'r') as zip_ref:
                        zip_ref.extractall(self.__emplacementSoft)
                        zip_ref.close()
                        try:
                            self.getSoftInstall()
                            if (linuxOs == True): # Mise en place du raccourci sur linux
                                os.remove(fileName)
                                nameExe = dictSoft["nameexelinux"]
                                # Creation du fichier lauch.sh qui permet de lancer le logiciel
                                with open(f"{self.__emplacementSoft}/{dictSoft['namefolderLinux']}/lauch.sh", "w") as file:
                                    file.write("#!/bin/bash\n"
                                               "cd "+self.__emplacementSoft+"/"+dictSoft['namefolderLinux']+
                                               "\n./"+nameExe)
                                    file.close()
                                # Rendu du logiciel executable et du fichier lauch.sh
                                os.chmod(f"{self.__emplacementSoft}/{dictSoft['namefolderLinux']}/lauch.sh",0o777)
                                os.chmod(f"{self.__emplacementSoft}/{dictSoft['namefolderLinux']}/{nameExe}",0o777)
                                # Ecrire le fichier .desktop
                                emplacementExe = self.__emplacementSoft + "/" + dictSoft['namefolderLinux'] + "/lauch.sh"
                                contentDesk = ("[Desktop Entry]" +
                                               "\nVersion=" + dictSoft["version"] +
                                               "\nType=Application" +
                                               "\nName=" + self.__formatNameApp(soft) +
                                               "\nExec=" + emplacementExe +
                                               "\nTerminal=false" +
                                               "\nStartupNotify=false")
                                # Ajouter l'icone si elle existe
                                if dictSoft["iconLinux"] != "":
                                    contentDesk += "\nIcon="+self.__emplacementSoft+"/"+dictSoft['namefolderLinux']+"/"+dictSoft["iconLinux"]
                                dir =  os.path.expanduser("~")+ "/.local/share/applications/"+soft+".desktop"
                                # Ecrire le fichier .desktop
                                with open(dir, "w") as file :
                                    file.write(contentDesk)
                                    file.close()

                                directorySoft = self.__emplacementSoft+"/"+dictSoft['namefolderLinux']

                            else :
                                if (windowsOS == True):
                                    # Importation de la librairy pour cree un raccourci
                                    import win32com.client
                                    # Suppression du fichier zip
                                    fileName = fileName.replace("/","\\")
                                    os.system(f'del /f /q "{fileName}"')
                                    # Creation de variable pour le raccourci
                                    emplacementExe = r""+self.__emplacementSoft+"/"+dictSoft["namefolderWin"]+"/"+dictSoft["nameexewin"]
                                    shorcutPath = r""+str(os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu','Programmes'))+"\\"+soft+".lnk"
                                    workFolder = r""+self.__emplacementSoft+"/"+dictSoft["namefolderWin"]

                                    # Debut creation raccourci
                                    shell = win32com.client.Dispatch("WScript.Shell")
                                    shortcut = shell.CreateShortCut(shorcutPath)
                                    shortcut.TargetPath =  os.path.join(emplacementExe)
                                    shortcut.WorkingDirectory = os.path.join(self.__emplacementSoft, dictSoft["namefolderWin"])
                                    shortcut.Description = self.__formatNameApp(soft)
                                    # Mise en place de l'icon du raccourci si elle existe
                                    icon = dictSoft["iconWin"]
                                    if (icon != ""):
                                        iconLnk = workFolder+"/"+icon
                                        shortcut.IconLocation = iconLnk
                                    # Sauvegarde du raccourci
                                    shortcut.save()
                                    directorySoft = self.__emplacementSoft+"/"+dictSoft["namefolderWin"]

                            # Ecriture du fichier de version
                            with open(f"{directorySoft}/VERSION", "w") as file:
                                file.write("VERSION="+dictSoft["version"]+"\n")
                                file.write("NAME="+soft.upper())
                                file.close()
                            self.__tigerFile.EcritureJSON(soft,emplacementExe)
                            return True
                        except FileNotFoundError:
                            return False
                        except PermissionError:
                            return False
                        except Exception as e:
                            return False

    def getSoftAvailable(self):
        listeSoft = []
        dictAllSoft = self.__depotFile.dictJson()
        listeAllSoft = list(dictAllSoft.keys())

        windowsOS = self.__system.osWindows()
        linuxOs = self.__system.osLinux()
        for i in range(0,len(listeAllSoft)):
            if (windowsOS == True and linuxOs == False
                    and dictAllSoft[listeAllSoft[i]]["namezipwin"]!=""
                    and dictAllSoft[listeAllSoft[i]]["linkWin"]!=""
                    and dictAllSoft[listeAllSoft[i]]["namefolderWin"]!=""):
                listeSoft.append(listeAllSoft[i])
            else :
                if (windowsOS == False and linuxOs == True
                        and dictAllSoft[listeAllSoft[i]]["nameziplinux"]!=""
                        and dictAllSoft[listeAllSoft[i]]["linkLinux"]!=""
                        and dictAllSoft[listeAllSoft[i]]["namefolderLinux"]!=""):
                    listeSoft.append(listeAllSoft[i])

        if (len(listeSoft) == 0):
            return ["error"]
        else :
            return listeSoft

    def getSoftInstall(self):
        if (self.__emplacementSoft == ""):
            return ["error"]
        else :
            softAvailable = self.getSoftAvailable()
            dictSoft = self.__depotFile.dictJson()
            windowsOS = self.__system.osWindows()
            linuxOs = self.__system.osLinux()
            listOut = []
            try:
                # Convertir le chemin en objet Path
                chemin_path = Path(self.__emplacementSoft).resolve()  # resolve() normalise le chemin
                # Vérifier si le chemin existe
                if not chemin_path.exists():
                    return ["le chemin {self.__emplacementSoft} n'existe pas"]
                # Lister uniquement les dossiers
                dossiers = [str(d) for d in chemin_path.iterdir() if d.is_dir()]

                for i in range(0,len(dossiers)):
                    if linuxOs == True:
                        dossiers[i] = (dossiers[i].replace
                                       (self.__emplacementSoft,"").replace
                                       ("/","").replace
                                       ("\\",""))
                    else :
                        if windowsOS == True:
                            emplacementsoft = self.__emplacementSoft.replace("/","\\")
                            dossiers[i] = (dossiers[i].replace
                                           (emplacementsoft,"").replace
                                           ("/","").replace
                                           ("\\",""))


                for i in range(0,len(softAvailable)):
                    if (windowsOS == True) and (dictSoft[softAvailable[i]]["namefolderWin"] in dossiers):
                        listOut.append(softAvailable[i])
                    else :
                        if (linuxOs == True) and (dictSoft[softAvailable[i]]["namefolderLinux"] in dossiers):
                            listOut.append(softAvailable[i])

                if (len(listOut) == 0):
                    self.__tigerFile.EcritureJSON("arrera-interface","nothing")
                    self.__tigerFile.EcritureJSON("ryley","nothing")
                    self.__tigerFile.EcritureJSON("six","nothing")
                    self.__tigerFile.EcritureJSON("arrera-raccourci","nothing")
                    self.__tigerFile.EcritureJSON("arrera-postite","nothing")
                    self.__tigerFile.EcritureJSON("arrera-video-download","nothing")
                    self.__tigerFile.EcritureJSON("arrera-copilote","nothing")
                    return ["Aucun logiciel installé"]
                else :
                    if ("arrera-interface" not in listOut):
                        self.__tigerFile.EcritureJSON("arrera-interface","nothing")

                    if ("ryley" not in listOut):
                        self.__tigerFile.EcritureJSON("ryley","nothing")

                    if ("six" not in listOut):
                        self.__tigerFile.EcritureJSON("six","nothing")

                    if ("arrera-raccourci" not in listOut):
                        self.__tigerFile.EcritureJSON("arrera-raccourci","nothing")

                    if ("arrera-postite" not in listOut):
                        self.__tigerFile.EcritureJSON("arrera-postite","nothing")

                    if ("arrera-video-download" not in listOut):
                        self.__tigerFile.EcritureJSON("arrera-video-download","nothing")

                    if ("arrera-copilote" not in listOut):
                        self.__tigerFile.EcritureJSON("arrera-copilote","nothing")

                    return listOut

            except PermissionError:
                return ["Erreur de permission pour accéder"]
            except Exception as e:
                return ["Une erreur s'est produite"]

    def uninstall(self,soft : str):
        if (soft == ""):
            return False
        else :
            softInstalled = self.getSoftInstall()
            if (soft in softInstalled):
                dictSofts = self.__depotFile.dictJson()
                dictSoft = dictSofts[soft]

                if (self.__system.osLinux() == True):
                    folder = self.__emplacementSoft+"/"+dictSoft["namefolderLinux"]
                    dir =  os.path.expanduser("~")+ "/.local/share/applications/"+soft+".desktop"
                    os.remove(dir)
                else :
                    if (self.__system.osWindows() == True):
                        folder = self.__emplacementSoft+"/"+dictSofts[soft]["namefolderWin"]
                        shorcutPath = r""+str(os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu','Programs'))+"\\"+soft+".lnk"
                        os.system(f'del /f /q "{shorcutPath}"')
                    else :
                        return False
                if os.path.exists(folder):
                    shutil.rmtree(folder)
                self.getSoftInstall()
                return True
            else :
                return False


    def __formatNameApp(self, nameApp:str):
        # Supprimer les tirets
        nameApp = nameApp.replace("-", " ")

        # Mettre la première lettre en majuscule
        nameApp = nameApp.capitalize()

        # Mettre la première lettre après chaque espace en majuscule
        nameApp = ' '.join(word.capitalize() for word in nameApp.split())

        return nameApp

    def getIMGSoft(self,soft):
        dictSoft = self.__depotFile.dictJson()
        return dictSoft[soft]["img"]


    def verifFileJson(self):
        print("bite")
        if (self.__emplacementSoft == ""):
            print("false")
            return False
        else :
            print("true")
            softAvailable = self.getSoftAvailable()
            dictSoft = self.__depotFile.dictJson()
            windowsOS = self.__system.osWindows()
            linuxOs = self.__system.osLinux()
            listOut = []

            try:
                # Convertir le chemin en objet Path
                chemin_path = Path(self.__emplacementSoft).resolve()  # resolve() normalise le chemin
                # Vérifier si le chemin existe
                if not chemin_path.exists():
                    return ["le chemin {self.__emplacementSoft} n'existe pas"]
                # Lister uniquement les dossiers
                dossiers = [str(d) for d in chemin_path.iterdir() if d.is_dir()]

                for i in range(0,len(dossiers)):
                    if linuxOs == True:
                        dossiers[i] = (dossiers[i].replace
                                       (self.__emplacementSoft,"").replace
                                       ("/","").replace
                                       ("\\",""))
                    else :
                        if windowsOS == True:
                            emplacementsoft = self.__emplacementSoft.replace("/","\\")
                            dossiers[i] = (dossiers[i].replace
                                           (emplacementsoft,"").replace
                                           ("/","").replace
                                           ("\\",""))


                for i in range(0,len(softAvailable)):
                    if (windowsOS == True) and (dictSoft[softAvailable[i]]["namefolderWin"] in dossiers):
                        listOut.append(softAvailable[i])
                    else :
                        if (linuxOs == True) and (dictSoft[softAvailable[i]]["namefolderLinux"] in dossiers):
                            listOut.append(softAvailable[i])

                if (len(listOut) == 0):
                    self.__tigerFile.EcritureJSON("arrera-interface","nothing")
                    self.__tigerFile.EcritureJSON("ryley","nothing")
                    self.__tigerFile.EcritureJSON("six","nothing")
                    self.__tigerFile.EcritureJSON("arrera-raccourci","nothing")
                    self.__tigerFile.EcritureJSON("arrera-postite","nothing")
                    self.__tigerFile.EcritureJSON("arrera-video-download","nothing")
                    self.__tigerFile.EcritureJSON("arrera-copilote","nothing")


                if ("arrera-interface" not in listOut):
                    self.__tigerFile.EcritureJSON("arrera-interface","nothing")

                if ("ryley" not in listOut):
                    self.__tigerFile.EcritureJSON("ryley","nothing")

                if ("six" not in listOut):
                    self.__tigerFile.EcritureJSON("six","nothing")

                if ("arrera-raccourci" not in listOut):
                    self.__tigerFile.EcritureJSON("arrera-raccourci","nothing")

                if ("arrera-postite" not in listOut):
                    self.__tigerFile.EcritureJSON("arrera-postite","nothing")

                if ("arrera-video-download" not in listOut):
                    self.__tigerFile.EcritureJSON("arrera-video-download","nothing")

                if ("arrera-copilote" not in listOut):
                    self.__tigerFile.EcritureJSON("arrera-copilote","nothing")

                return True

            except PermissionError:
                return False
            except Exception as e:
                return False