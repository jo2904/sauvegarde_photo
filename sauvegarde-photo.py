from datetime import date
import os
import shutil
from tkinter import filedialog
from tkinter import *

#FONCTION

def lister(repertoire, numero):
    #Elaboration de l'arborescence
    espace = ''
    for n in range(0,numero):
        espace += '-----'

    for element in os.listdir(repertoire):  # Lecture repertoire
        if os.path.isdir(os.path.join(repertoire, element)):  # si dossier
            monfichier = open(Titre, 'a', newline=None)

            chaine = espace + "+" + element             #ajout path au caractere 400
            n = len(chaine)
            vide = ''
            for z in range(1, 400-n):
                vide += ' '
            chaine = chaine + vide + repertoire + '\\' + element

            monfichier.write("\n"+ chaine + "\n")
            monfichier.close
            lister(repertoire+'\\'+element, numero+1)         # analyse sous dossier 
        else:                       #si fichier
            monfichier = open(Titre, 'a', newline=None)

            chaine = espace + element  # ajout path au caractere 400
            n = len(chaine)
            vide = ''
            for z in range(1, 400-n):
                vide += ' '
            chaine = chaine + vide + repertoire + '\\' + element

            monfichier.write("\n" + chaine)
            monfichier.close

def inverse(titre):
    #inverse pour arborescence compréhensible
    f = open(Titre, 'r')
    tout = f.readlines()
    f.close()
    tout.reverse()

    t = open(Titre, 'w')
    for line in tout:
        t.write(line)
    t.close()

def recherche_rapport(repertoire):
    for element in os.listdir(repertoire):
        if element[0:11] == 'rapport_du_':
            return str(repertoire + '\\' + element)
    return 'False'

def copie(repertoire_racine, element_init, repertoire_sauvegarde):
    n = len(repertoire_racine)
    fichier = element_init[n:len(element_init)-1]          #copie path_element - racine
    #copie dans fichier de sauvegarde
    if os.path.isdir(repertoire_racine+'\\'+fichier): #os.path.join(repertoire, element)): #si dossier
        commande = 'xcopy "'+repertoire_racine+'\\'+fichier+ '" "' + repertoire_sauvegarde+'\\'+fichier+'" /S /I /Q /Y /F /T'
        os.system(commande)
    else: #si fichier
        commande = 'copy "'+repertoire_racine+'\\'+fichier+ '" "' + repertoire_sauvegarde+'\\'+fichier+'" /Y'
        os.system(commande)
        


def comparer_copie(repertoire, repertoire_sauvegarde, rapport_init, rapport_copie):
    rapport_init_txt = open(rapport_init, 'r')   #Ouverture des deux rapports
    rapport_sauvegarde_txt = open(rapport_copie, 'r')
    lines = rapport_init_txt.readlines()        #lecture des deux rapports
    lines2 = rapport_sauvegarde_txt.readlines()
    rapport_init_txt.close()            #fermeture des rapport
    rapport_sauvegarde_txt.close()
    for line in lines:                  #recherche si doc existe dans autre
        for line2 in lines2:
            if line[400:len(line)+1] == line2[400:len(line2)+1]:#compare les path
                break               #si oui => ignorer
            if line2[0:4] == 'fin':
                copie(repertoire, line[400:len(line)+1], repertoire_sauvegarde)
                

def copie_rapport_fin(titre, repertoire_sauvegarde):
    # copie dans fichier de sauvegarde
    f = open(Titre, 'a')  #ajout fin
    f.write('fin')
    f.close()
    filePath = shutil.copy('INFORMATION_COPIE.txt', repertoire_sauvegarde)
    filePath = shutil.copy(titre, repertoire_sauvegarde)


def mode_d_emploie():
    os.system('start https://github.com/jo2904/sauvegarde_photo')

#MAIN
def main():

    #INIT
    Repertoire = fenetre.filename = filedialog.askdirectory(initialdir="C:\\Users", title="Fichier à sauvegarder")
    Repertoire_sauvegarde = fenetre.filename = filedialog.askdirectory(initialdir="C:\\Users", title="Fichier de sauvegarde")

    #RECUPERATION DATE PUIS CREATION TITRE ET NOM RAPPORT 
    today = str(date.today())

    Titre = 'rapport_du_' + today + '.txt'

    for element in os.listdir(Repertoire):
        if element == Titre:
            os.remove(Titre)
        else:
            break
    
    #Creation page information
    f = open('INFORMATION_COPIE.txt', 'w')
    f.write(today + '\n' + 'copie de ' + Repertoire +' dans '+ Repertoire_sauvegarde)
    f.close()


    #création nouveau
    f = open(Titre, 'w')
    f.write('')
    f.close()

    #Debut procédure    
    label = Label(fenetre, text="Chargement en cours")
    label.pack()
    
    lister(Repertoire, 0)

    inverse(Titre)

    label = Label(fenetre, text="Liste OK")
    label.pack()

    rapport_sauvegarde = str(recherche_rapport(Repertoire_sauvegarde))

    label = Label(fenetre, text="rapport ")
    label.pack()

    if rapport_sauvegarde == 'False':  #Si pas de rapport tt copier
        label = Label(fenetre, text="Copie simple...")
        label.pack()
        commande = 'xcopy "'+Repertoire+ '" "' + Repertoire_sauvegarde+'" /S /Y'
        os.system(commande)
    elif rapport_sauvegarde[len(rapport_sauvegarde)-3:len(rapport_sauvegarde)+1] == 'txt':
        #Sinon compare et copie
        label = Label(fenetre, text="Copie après comparaison...")
        label.pack()
        comparer_copie(Repertoire, Repertoire_sauvegarde, Titre, rapport_sauvegarde)

    for element in os.listdir(Repertoire_sauvegarde):           #supprime ancien rapport
        if element[0:11] == 'rapport_du_':
            os.remove(Repertoire_sauvegarde+'\\'+element)

    label = Label(fenetre, text="enregistrement du rapport...")
    label.pack()
    copie_rapport_fin(Titre, Repertoire_sauvegarde) #copie nouveau rapport

    label = Label(fenetre, text="la sauvegarde est terminée")
    label.pack()


#FENETRE
    
fenetre = Tk()
fenetre.title("Sauvegarde ")
fenetre.geometry("400x300")

label = Label(fenetre, text="Sauvegarde des photos (par JdG)")
label.pack()

btn = Button(fenetre, text = 'Mode d \'emploie', command = mode_d_emploie)
btn.pack()

btn2 = Button(fenetre, text = 'Démarrer', command = main)
btn2.pack()

fenetre.mainloop()
