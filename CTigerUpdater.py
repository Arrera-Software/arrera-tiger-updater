from librairy.arrera_tk import *
from CArreraTiger import *
import socket
import tkinter.messagebox as mbox
import threading as th
import tkinter.filedialog as fd

class CTigerUpdater:
    def __init__(self):
        # Initialisation des objet de la classe
        self.__arrTk = CArreraTK()
        self.__tiger = CArreraTiger("config.json")
        # Creation de la varriable pour le theard
        self.__thread = th.Thread()
        # Chargement des images
        imageSoft = self.__arrTk.createImage("img/arrera-tiger.png",
                                             "img/arrera-tiger.png",
                                             tailleX=100,tailleY=100)
        # Creation de la fenetre
        self.__rootWin = self.__arrTk.aTK(title="Installateur d'Arrera Store",width=500,height=400)
        # Frame de la fenetre
        self.__fAcceuil = self.__arrTk.createFrame(self.__rootWin,width=450,height=350,bg="red")
        self.__fInstall = self.__arrTk.createFrame(self.__rootWin,width=450,height=350,bg="blue")
        # Widget de la fenetre
        # fAcceuil
        labelIMGSoft = self.__arrTk.createLabel(self.__fAcceuil,text="",image=imageSoft)
        labelTextSoft = self.__arrTk.createLabel(self.__fAcceuil,text="Installateur d'Arrera Store"
                                                 ,ppolice="Arial",ptaille=20,pstyle="bold")
        btnInstall = self.__arrTk.createButton(self.__fAcceuil,text="Installer",
                                               ppolice="Arial",ptaille=15,pstyle="bold",
                                               command=self.__install)
        btnUpdate = self.__arrTk.createButton(self.__fAcceuil,text="Mettre à jour",
                                              ppolice="Arial",ptaille=15,pstyle="bold")

        # fInstall
        self.__labelInstall = self.__arrTk.createLabel(self.__fInstall,text="Installation en cours",
                                                       ppolice="Arial",ptaille=15,pstyle="bold")


        # Affichage des widget
        self.__arrTk.placeCenter(self.__fAcceuil)
        self.__arrTk.placeTopCenter(labelIMGSoft)
        self.__arrTk.placeCenter(labelTextSoft)
        self.__arrTk.placeBottomLeft(btnInstall)
        self.__arrTk.placeBottomRight(btnUpdate)
        self.__arrTk.placeCenter(self.__labelInstall)

    def start(self):
        # Vérification de la connexion internet
        if (self.__testConnectInternet()==False):
            mbox.showerror("Erreur", "Pas de connexion internet")
            return
        # Load du depots
        if (self.__tiger.loadDepots("https://arrera-software.fr/depots.json") == False):
            mbox.showerror("Erreur", "Erreur lors du chargement des dépôts")
            return


        self.__arrTk.view()

    def __testConnectInternet(self):
        try:
            # Tente de se connecter au serveur
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8",53))
            return True
        except socket.error:
            return False

    def __install(self):
        mbox.showinfo("Information",
                      "Sélectionnez l'emplacement où vous souhaitez installer Arrera Store.")
        directory = fd.askdirectory()
        while directory == "":
            mbox.showerror("Erreur", "Veuillez sélectionner un emplacement valide.")
            directory = fd.askdirectory()

        sortieFolder = self.__tiger.setEmplacementArreraSoft(directory)
        if (sortieFolder == True):
            mbox.showinfo("Information", "Emplacement selectionné avec succès.")
        else:
            mbox.showerror("Erreur", "Erreur lors de l'enregistrement de l'emplacement.")
            return False

        # Lancement de l'installation
        self.__thread = th.Thread(target=self.__tiger.install, args=("arrera-tiger",))
        self.__thread.start()
        self.__fAcceuil.place_forget()
        self.__arrTk.placeCenter(self.__fInstall)
        self.__rootWin.after(100, self.__checkInstall)
        return True

    def __checkInstall(self):
        if (self.__thread.is_alive()):
            text = self.__labelInstall.cget("text")
            newText = text + "."
            self.__labelInstall.configure(text=newText)
            self.__rootWin.after(100, self.__checkInstall)
        else:
            mbox.showinfo("Information", "Installation terminée avec succès.")
            self.__rootWin.destroy()