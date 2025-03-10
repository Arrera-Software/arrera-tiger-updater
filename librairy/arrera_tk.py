import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
import webbrowser as wb
import platform
import os
from typing import Union

VERSIONARRERATK = "1.0.0"

class CArreraTK :
    def __init__(self):
        self.__mode = 0
        self.__windowsColor = ""
        self.__textColor = ""
        self.__images = []

    def aTK(self, mode: int = 0, width: int = 800, height: int = 600,title: str = "ArreraTK", resizable: bool = False, bg: str = "", fg: str = "", icon: str = ""):
        """
        :param mode: 1 for Tkinter, 0 for customtkinter
        :param mainWindow: True for main window, False for Toplevel
        :param width: width of the window
        :param height: height of the window
        :param title: title of the window
        :param resizable: True for resizable, False for not resizable
        :param bg:  background color
        :param fg:  text color
        :param icon: icon of the window (ico file)
        """
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        ctheme = ctk.get_appearance_mode()
        if ctheme == "Dark":
            defaultColor = ctk.ThemeManager.theme["CTk"]["fg_color"][1]
            defaultTextColor = ctk.ThemeManager.theme["CTk"]["fg_color"][0]
        else:
            defaultColor = ctk.ThemeManager.theme["CTk"]["fg_color"][0]
            defaultTextColor = ctk.ThemeManager.theme["CTk"]["fg_color"][1]
        self.__mode = mode
        if mode == 0:
            self.__root = ctk.CTk()
            self.__root.configure(fg_color=defaultColor)
        else:
            self.__root = Tk()
        if icon != "":
            if platform.system() == "Windows":
                if os.path.splitext(icon)[1].lower() == '.ico' :
                    self.__root.iconbitmap(icon)
            else:
                if os.path.splitext(icon)[1].lower() == '.png' :
                    self.__root.iconphoto(True, PhotoImage(file=icon))
        self.__root.geometry(f"{width}x{height}")
        self.__root.title(title)
        self.__root.resizable(resizable, resizable)
        if bg == "":
            self.__root.configure(bg=defaultColor)
            self.__windowsColor = defaultColor
            self.__textColor = defaultTextColor
        else:
            self.__root.configure(bg=bg)
            self.__windowsColor = bg
            self.__textColor = fg

        return self.__root

    def aTopLevel(self, mode: int = 0, width: int = 800, height: int = 600,title: str = "ArreraTK", resizable: bool = False, bg: str = "", fg: str = "", icon: str = ""):
        """
        :param mode: 1 for Tkinter, 0 for customtkinter
        :param mainWindow: True for main window, False for Toplevel
        :param width: width of the window
        :param height: height of the window
        :param title: title of the window
        :param resizable: True for resizable, False for not resizable
        :param bg:  background color
        :param fg:  text color
        :param icon: icon of the window (ico file)
        """
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        ctheme = ctk.get_appearance_mode()
        if ctheme == "Dark":
            defaultColor = ctk.ThemeManager.theme["CTk"]["fg_color"][1]
            defaultTextColor = ctk.ThemeManager.theme["CTk"]["fg_color"][0]
        else:
            defaultColor = ctk.ThemeManager.theme["CTk"]["fg_color"][0]
            defaultTextColor = ctk.ThemeManager.theme["CTk"]["fg_color"][1]
        self.__mode = mode
        if mode == 0:
            self.__root = ctk.CTkToplevel()
        else:
            self.__root = Toplevel()
        if icon != "":
            if platform.system() == "Windows":
                if os.path.splitext(icon)[1].lower() == '.ico':
                    self.__root.iconbitmap(icon)
            else:
                if os.path.splitext(icon)[1].lower() == '.png':
                    self.__root.iconphoto(True, PhotoImage(file=icon))
        self.__root.geometry(f"{width}x{height}")
        self.__root.title(title)
        self.__root.resizable(resizable, resizable)
        if bg == "":
            self.__root.configure(fg_color=defaultColor)
            self.__windowsColor = defaultColor
            self.__textColor = defaultTextColor
        else:
            self.__root.configure(fg_color=bg)
            self.__windowsColor = bg
            self.__textColor = fg

        return self.__root

    def view(self):
        self.__root.mainloop()

    def title(self, title: str):
        self.__root.title(title)

    def setGeometry(self, width: int, height: int):
        self.__root.geometry(f"{width}x{height}")

    def setResizable(self, resizable: bool):
        self.__root.resizable(resizable, resizable)

    def setColor(self, bg: str, fg: str):
        self.__root.configure(bg=bg)
        self.__windowsColor = bg
        self.__textColor = fg


    def createImage(self, pathLight: str, pathDark: str = "none", tailleX: int = 250, tailleY: int = 250):
        if (self.__mode == 0):
            if (pathDark != "none"):
                image = ctk.CTkImage(
                    light_image=Image.open(pathLight),
                    dark_image=Image.open(pathDark),
                    size=(tailleX, tailleY))
                return image
            else :
                image = ctk.CTkImage(
                    light_image=Image.open(pathLight),
                    size=(tailleX, tailleY))
                return image
        else :
            if (pathDark != "none"):
                imageLight = PhotoImage(file=pathLight)
                imageDark = PhotoImage(file=pathDark)
                return [imageLight, imageDark]
            else :
                imageLight = PhotoImage(file=pathLight)
                return imageLight

    def createLabel(self, screen, text: str = "", image : Union[ctk.CTkImage, PhotoImage] = None, bg : str = "", fg : str = "", ppolice : str = "Arial", ptaille : int = 12,pstyle : str = "normal",width : int = 0,height : int = 0,pwraplength : int = 0,justify : str = "center"):
        if (self.__mode == 0):
            label = ctk.CTkLabel(screen)
            if (text != ""):
                label.configure(text=text)
            if (image != None):
                label.configure(image=image)
                label.configure(text="")
            if (fg != ""):
                label.configure(text_color=fg)
            if (bg != ""):
                label.configure(fg_color=bg)
            if (width != 0):
                label.configure(width=width)
            if (height != 0):
                label.configure(height=height)
            if (pwraplength != 0):
                label.configure(wraplength=pwraplength)
            police = "Arial"
            style = "normal"
            taille = 12
            if (ppolice != "Arial"):
                police = ppolice
            if (ptaille != 12):
                taille = ptaille
            if (pstyle != "normal" and (pstyle == "bold" or pstyle == "italic" or pstyle == "underline")):
                style = pstyle
            if (image != None):
                label.configure(image=image)
            label.configure(font=(police, taille, style),justify=justify)
        else :
            label = Label(screen)
            if (text != ""):
                label.configure(text=text)
            if (image != None):
                label.configure(image=image)
            if (bg != ""):
                label.configure(bg=bg)
            if (fg != ""):
                label.configure(fg=fg)
            if (width != 0):
                label.configure(width=width)
            if (height != 0):
                label.configure(height=height)
            if (pwraplength != 0):
                label.configure(wraplength=pwraplength)
            if (ppolice != "Arial" or ptaille != 12):
                label.configure(font=(ppolice, ptaille))
        return label

    def createButton(self, screen, text: str = "", image = None, bg : str = "", fg : str = "", command = None,ppolice : str = "Arial", ptaille : int = 12,pstyle :str = "normal",width : int = 0,height : int = 0,hoverbg:str=""):
        if (self.__mode == 0):
            btn = (ctk.CTkButton(screen))
            if (text != ""):
                btn.configure(text=text)
            else :
                btn.configure(text="")
            if (image != None):
                btn.configure(image=image)
                btn.configure(text="")
            if (fg != ""):
                btn.configure(text_color=fg)
            if (bg != ""):
                btn.configure(fg_color=bg)
            if (hoverbg != ""):
                btn.configure(hover_color=hoverbg)
            if (command != None):
                btn.configure(command=command)
            if (width != 0):
                btn.configure(width=width)
            if (height != 0):
                btn.configure(height=height)
            police = "Arial"
            style = "normal"
            taille = 12
            if (ppolice != "Arial"):
                police = ppolice
            if (ptaille != 12):
                taille = ptaille
            if (pstyle != "normal" and (pstyle == "bold" or pstyle == "italic" or pstyle == "underline")):
                style = pstyle

            btn.configure(font=(police,taille,style))

        else :
            btn = Button(screen)
            if (text != ""):
                btn.configure(text=text)
            else :
                btn.configure(text="")
            if (image != None):
                btn.configure(image=image)
            if (bg != ""):
                btn.configure(bg=bg)
            if (fg != ""):
                btn.configure(fg=fg)
            if (command != None):
                btn.configure(command=command)
            if (ppolice != "Arial" or ptaille != 12):
                btn.configure(font=(ppolice, ptaille))
            if (width != 0):
                btn.configure(width=width)
            if (height != 0):
                btn.configure(height=height)
        return btn

    def createEntry(self, screen, bg : str = "", fg : str = "", placeholderText :str = "", ppolice : str = "Arial", ptaille : int = 12, width : int = 20):
        if (self.__mode == 0):
            entry = ctk.CTkEntry(screen)
            if (fg != ""):
                entry.configure(text_color=fg)
            if (bg != ""):
                entry.configure(fg_color=bg)
            if (placeholderText != ""):
                entry.configure(placeholder_text=placeholderText)
            if (ppolice != "Arial" or ptaille != 12):
                entry.configure(font=(ppolice, ptaille, "normal"))
            if (width != 20):
                entry.configure(width=width)
        else :
            entry = Entry(screen)
            if (bg != ""):
                entry.configure(bg=bg)
            if (fg != ""):
                entry.configure(fg=fg)
            if (ppolice != "Arial" or ptaille != 12):
                entry.configure(font=(ppolice, ptaille))
        return entry

    def createText(self, screen, bg : str = "", fg : str = ""):
        text = Text(screen)
        if (bg != ""):
            text.configure(bg=bg)
        if (fg != ""):
            text.configure(fg=fg)

        return text

    def createCheckbox(self, screen, text: str = "", bg : str = "", fg : str = ""):
        checkbox = Checkbutton(screen,text=text)
        if (bg != ""):
            checkbox.configure(bg=bg)
        if (fg != ""):
            checkbox.configure(fg=fg)
        return checkbox

    def createRadioButton(self, screen, text: str = "", bg : str = "", fg : str = ""):
        if (self.__mode == 0):
            radio = ctk.CTkRadioButton(screen)
            if (text != ""):
                radio.configure(text=text)
            if (bg != ""):
                radio.configure(bg_color=bg)
            if (fg != ""):
                radio.configure(fg_color=fg)
        else :
            radio = Radiobutton(screen,text=text)
            if (bg != ""):
                radio.configure(bg=bg)
            if (fg != ""):
                radio.configure(fg=fg)
        return radio

    def createCanvas(self, screen, width: int, height: int, bg : str = "",imageFile : str = ""):
        canvas = Canvas(screen, width=width, height=height)
        if (bg != ""):
            canvas.configure(bg=bg)
        if (imageFile != ""):
            photo = PhotoImage(file=imageFile,master=canvas)
            canvas.image_names = photo
            canvas.create_image(0, 0, image=photo, anchor="nw")
        return canvas

    def createFrame(self, screen,width : int = 0 ,height : int = 0,  bg : str = "",wightBoder : int = 0,corner_radius : int = 1024):
        if (self.__mode == 0):
            frame = ctk.CTkFrame(screen)
            if (width != 0):
                frame.configure(width=width)
            if (height != 0):
                frame.configure(height=height)
            if (bg != ""):
                frame.configure(fg_color=bg)
            else:
                frame.configure(fg_color=self.__windowsColor)
            if (wightBoder != 0):
                frame.configure(border_width=wightBoder)
            if (corner_radius != 1024):
                frame.configure(corner_radius=corner_radius)
            frame.update()
        else :
            frame = Frame(screen)
            if (width != 0):
                frame.configure(width=width)
            if (height != 0):
                frame.configure(height=height)
            if (bg != ""):
                frame.configure(bg=bg)
            if (wightBoder != 0):
                frame.configure(borderwidth=wightBoder,relief="solid")
        return frame

    def createOptionMenu(self,screen,value: list, var:StringVar,taille : int = 0, police :str = "" ):
        if (self.__mode == 0):
            option = ctk.CTkOptionMenu(screen,variable=var,values=value)
        else:
            option = OptionMenu(screen,var,*value)
        if (police != "" and taille != 0):
            option.configure(font=(police,taille,"normal"))
        var.set(value[0])
        return option

    def placeLeftTop(self, widget):
        widget.place(relx=0, rely=0, anchor='nw')

    def placeRightTop(self, widget):
        widget.place(relx=1, rely=0, anchor='ne')

    def placeLeftBottom(self, widget):
        widget.place(relx=0, rely=1, anchor='sw')

    def placeRightBottom(self, widget):
        widget.place(relx=1, rely=1, anchor='se')

    def placeCenter(self, widget):
        widget.place(relx=0.5, rely=0.5, anchor='center')

    def placeLeftCenter(self, widget):
        widget.place(relx=0, rely=0.5, anchor='w')

    def placeRightCenter(self, widget):
        widget.place(relx=1, rely=0.5, anchor='e')

    def placeTopCenter(self, widget):
        widget.place(relx=0.5, rely=0, anchor='n')

    def placeBottomCenter(self, widget):
        widget.place(relx=0.5, rely=1, anchor='s')

    def placeCenterOnWidth(self,widget,y :int = 0 ):
        if (y==0):
            return False
        else :
            widget.place(relx=0.5, y=y, anchor='n')

    def placeBottomRight(self,widget):
        widget.place(relx=1, rely=1, anchor='se')

    def placeBottomLeft(self,widget):
        widget.place(relx=0, rely=1, anchor='sw')

    def placeTopRight(self,widget):
        widget.place(relx=1, rely=0, anchor='ne')

    def placeTopLeft(self,widget):
        widget.place(relx=0, rely=0, anchor='nw')

    def placeCenterRight(self,widget):
        widget.place(relx=1, rely=0.5, anchor='e')

    def placeCenterLeft(self,widget):
        widget.place(relx=0, rely=0.5, anchor='w')

    def pack(self, widget,xExpand : bool = False , yExpand : bool = False):
        if (xExpand and yExpand):
            widget.pack(expand="both")
        else:
            if (xExpand):
                widget.pack(expand="x")
            else:
                if (yExpand):
                    widget.pack(expand="y")
                else:
                    widget.pack()

    def packLeft(self, widget,xExpand : bool = False , yExpand : bool = False):
        if (xExpand and yExpand):
            widget.pack(expand="both",side="left")
        else:
            if (xExpand):
                widget.pack(expand="x",side="left")
            else:
                if (yExpand):
                    widget.pack(expand="y",side="left")
                else:
                    widget.pack(side="left")

    def packRight(self, widget,xExpand : bool = False , yExpand : bool = False):
        if (xExpand and yExpand):
            widget.pack(expand="both",side="right")
        else:
            if (xExpand):
                widget.pack(expand="x",side="right")
            else:
                if (yExpand):
                    widget.pack(expand="y",side="right")
                else:
                    widget.pack(side="right")

    def packTop(self, widget,xExpand : bool = False , yExpand : bool = False):
        if (xExpand and yExpand):
            widget.pack(expand="both",side="top")
        else:
            if (xExpand):
                widget.pack(expand="x",side="top")
            else:
                if (yExpand):
                    widget.pack(expand="y",side="top")
                else:
                    widget.pack(side="top")

    def packBottom(self, widget,xExpand : bool = False , yExpand : bool = False):
        if (xExpand and yExpand):
            widget.pack(expand="both",side="bottom")
        else:
            if (xExpand):
                widget.pack(expand="x",side="bottom")
            else:
                if (yExpand):
                    widget.pack(expand="y",side="bottom")
                else:
                    widget.pack(side="bottom")

    def aproposWindows(self,nameSoft:str,iconFile:str,version:str,copyright:str,linkSource:str,linkWeb:str):
        if (self.__mode == 0):
            apropos = ctk.CTkToplevel()
            apropos.configure(bg=self.__windowsColor)
            apropos.title("A propos : "+nameSoft)
            apropos.maxsize(400,300)
            apropos.minsize(400,300)
            icon = ctk.CTkImage(light_image=Image.open(iconFile),size=(100,100))
            mainFrame = ctk.CTkFrame(apropos,width=400,height=250,border_width=0,fg_color=self.__windowsColor)
            frameBTN = ctk.CTkFrame(apropos,width=400,height=50,border_width=0,fg_color=self.__windowsColor)
            frameLabel = ctk.CTkFrame(apropos,border_width=0,fg_color=self.__windowsColor)

            labelIcon = ctk.CTkLabel(mainFrame,image=icon,text="",fg_color=self.__windowsColor)
            labelSoft = ctk.CTkLabel(frameLabel,text=nameSoft+" version "+version,font=("Arial",20),fg_color=self.__windowsColor)
            labelVersion = ctk.CTkLabel(frameLabel,text="Arrera TK version "+VERSIONARRERATK,font=("Arial",13),fg_color=self.__windowsColor)
            labelCopy = ctk.CTkLabel(mainFrame,text=copyright,font=("Arial",13),fg_color=self.__windowsColor)

            btnLinkSource = ctk.CTkButton(frameBTN,text="Source code",command= lambda :  wb.open(linkSource))
            btnLinkWeb = ctk.CTkButton(frameBTN,text="Web site",command= lambda :  wb.open(linkWeb))

            labelIcon.place(relx=0.5, rely=0.0, anchor="n")
            labelSoft.pack()
            labelVersion.pack()
            labelCopy.place(relx=0.5, rely=1.0, anchor="s")

            frameLabel.place(relx=0.5, rely=0.5, anchor="center")
            mainFrame.pack(side="top")
            frameBTN.pack(side ="bottom")


            btnLinkSource.place(relx=1, rely=1, anchor='se')
            btnLinkWeb.place(relx=0, rely=1, anchor='sw')
        else :
            apropos = Toplevel()
            apropos.title("A propos : " + nameSoft)
            apropos.configure(bg=self.__windowsColor)
            apropos.maxsize(400, 300)
            apropos.minsize(400, 300)
            icon = ctk.CTkImage(light_image=Image.open(iconFile), size=(100, 100))
            mainFrame = Frame(apropos, width=400, height=250,bg=self.__windowsColor)
            frameBTN = Frame(apropos, width=400, height=50,bg=self.__windowsColor)
            frameLabel = Frame(apropos,bg=self.__windowsColor)

            # Traitement Image
            labelIcon = Label(mainFrame, bg=self.__windowsColor)
            imageOrigine = Image.open(iconFile)
            imageRedim = imageOrigine.resize((100,100))
            icon = ImageTk.PhotoImage(imageRedim, master=labelIcon)
            labelIcon.image_names = icon
            labelIcon.configure(image=icon)

            labelSoft = Label(frameLabel, text=nameSoft + " version " + version, font=("Arial", 20),bg=self.__windowsColor,fg=self.__textColor)
            labelVersion = Label(frameLabel, text="Arrera TK version " + VERSIONARRERATK, font=("Arial", 13),bg=self.__windowsColor,fg=self.__textColor)
            labelCopy = Label(mainFrame, text=copyright, font=("Arial", 13),bg=self.__windowsColor,fg=self.__textColor)

            btnLinkSource = Button(frameBTN, text="Source code", command=lambda: wb.open(linkSource),bg=self.__windowsColor,fg=self.__textColor)
            btnLinkWeb = Button(frameBTN, text="Web site", command=lambda: wb.open(linkWeb),bg=self.__windowsColor,fg=self.__textColor)

            labelIcon.place(relx=0.5, rely=0.0, anchor="n")
            labelSoft.pack()
            labelVersion.pack()
            labelCopy.place(relx=0.5, rely=1.0, anchor="s")

            frameLabel.place(relx=0.5, rely=0.5, anchor="center")
            mainFrame.pack(side="top")
            frameBTN.pack(side="bottom")

            btnLinkSource.place(relx=1, rely=1, anchor='se')
            btnLinkWeb.place(relx=0, rely=1, anchor='sw')

    def createTopMenu(self,master:Union[Tk,ctk.CTk, Toplevel, ctk.CTkToplevel,Menu]):
        newMenu = Menu(master, tearoff=0, bg=self.__windowsColor, fg=self.__textColor)
        if isinstance(master, (Tk, ctk.CTk, Toplevel, ctk.CTkToplevel)):
            master.configure(menu=newMenu)
        return newMenu

    def addCommandTopMenu(self,menu:Menu,command,text:str):
        menu.add_command(label=text,command=command)

    def addCascadeTopMenu(self, menuMaster:Menu, menuChild:Menu, text:str):
        menuMaster.add_cascade(label=text, menu=menuChild)

    def createArreraBackgroudImage(self,screen:Union[Tk,ctk.CTk,Toplevel,ctk.CTkToplevel],imageLight:str,imageDark :str = "",height:int = 600,width:int = 800):
        if (self.__mode == 0):
            if (imageDark != ""):
                image = ctk.CTkImage(light_image=Image.open(imageLight),
                                     dark_image=Image.open(imageDark),
                                     size=(width, height))
            else :
                image = ctk.CTkImage(light_image=Image.open(imageLight)
                                     ,size=(width, height))
            frame = ctk.CTkFrame(screen,width=width,height=height,border_width=0)
            label = ctk.CTkLabel(frame,image=image,text="")
            label.place(relx=0.5, rely=0.5, anchor='center')
            return frame

    def labelChangeColor(self,label : Union[Label,ctk.CTkLabel],bg:str = "" ,fg :str = "" ):
        if isinstance (label,Label):
            if (bg != ""):
                label.configure(bg=bg)
            if (fg != ""):
                label.configure(fg=fg)
        else:
            if (fg != ""):
                label.configure(text_color=fg)
            if (bg != ""):
                label.configure(fg_color=bg)

    def boutonChangeColor(self, button : Union[Button,ctk.CTkButton], bg:str, fg:str ="",hoverbg:str=""):
        if isinstance (button, Button):
            if (bg != ""):
                button.configure(bg=bg)
            if (fg != ""):
                button.configure(fg=fg)
        else:
            if (fg != ""):
                button.configure(text_color=fg)
            if (bg != ""):
                button.configure(fg_color=bg)
            if (hoverbg != ""):
                button.configure(hover_color=hoverbg)

    def getTheme(self):
        return ctk.get_appearance_mode()

    def createTextBox(self,screen:Union[Tk,ctk.CTk,Toplevel,ctk.CTkToplevel],width:int = 0,height:int = 0,bg:str = "",fg:str = "",ppolice:str="Arial",ptaille:int=12,pstyle:str="normal",wrap:str="word"):
        if (self.__mode == 0):
            text = ctk.CTkTextbox(screen)
            if (fg != ""):
                text.configure(text_color=fg)
            if (bg != ""):
                text.configure(fg_color=bg)
            if (width != 0):
                text.configure(width=width)
            if (height != 0):
                text.configure(height=height)

            police = "Arial"
            style = "normal"
            taille = 12

            if (ppolice != "Arial"):
                police = ppolice
            if (ptaille != 12):
                taille = ptaille
            if (pstyle != "normal" and (pstyle == "bold" or pstyle == "italic" or pstyle == "underline")):
                style = pstyle

            text.configure(font=(police, taille, style),wrap=wrap)

        else :
            text = Text(screen,width=width,height=height,bg=bg,fg=fg)
            if (fg != ""):
                text.configure(fg=fg)
            if (bg != ""):
                text.configure(bg=bg)
            if (width != 0):
                text.configure(width=width)
            if (height != 0):
                text.configure(height=height)

            police = "Arial"
            style = "normal"
            taille = 12

            if (ppolice != "Arial"):
                police = ppolice
            if (ptaille != 12):
                taille = ptaille
            if (pstyle != "normal" and (pstyle == "bold" or pstyle == "italic" or pstyle == "underline")):
                style = pstyle

            text.configure(font=(police, taille, style))

        text.configure(state="disabled")
        return text

    def insertTextOnTextBox(self,textbox:Union[Text,ctk.CTkTextbox],text:str):
        textbox.configure(state="normal")
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")
