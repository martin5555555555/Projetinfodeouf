# -*- coding: utf-8 -*-


from ProtoV2 import *
from maq20 import MAQ20


from time import time
from datetime import datetime
from math import *

######### MAP DES CARTE D'ACQUISITION ET CONTROLE ############
from mapV2 import * #toutes les variables pour trouver les bons capteurs

##############################################################################
diameter=0.315 #TODO indiquer la bonne valeur
section = 1*pi*(diameter/2)**2 #0.8165
cp_air = 1005 #TODO indiquer la bonne valeur
rho_air = 1.29  #TODO indiquer la bonne valeur 
print_it=3



maq20_d=None
Restart=True
nbofattempt=0
while(Restart):
    try:
        maq20_d = MAQ20(ip_address="192.168.128.100", port=502)
        Restart=False
    except:
        Restart=True
        print("Error connection... Trying again")
        sleep(0.1)
        nbofattempt+=1
        if(nbofattempt>20):
            print("Timeout : too many unsuccessfull attempts")
            raise ValueError
#l'addresse IP pour la module COM2
#############################################################################

#Fonctions 

#Initialisation des differentes valeurs

Ini_time=str(datetime.now()).split(",")[0].replace("-", "_")
Ini_time=Ini_time.replace(":", "_")
deltaP = []
deb = []
p_vent = 0

###############################################################################
###############################################################################

#initialisation
    
##############################################################################
#Boucle d'input/print

count=0;

while True :
    current_time=('init_'+str(count))
    
    
    
    #Affichage
    
    for i in range (print_it):

        wait=5
        print('Please wait for '+str(wait)+' second(s)')
        
        sleep(wait)

        print("debit : "+str(section * sqrt(P2.get_value(maq20_d,current_time)*2/rho_air)*3600)+" m^3/h")
        print("surpression" + str(P1.get_value(maq20_d,current_time)))
        
        
           

    choice=input('Ecrire "start" pour demarer le code :')
    
    if choice=='start':
        
        name_file='Initialisation_Values_'+Ini_time+'.csv'
        fichier_acq=open(name_file, 'w')
        fichier_acq.write("date_time;puissance ventilateur - [%];deltaP - [Pa];debit_air - [m^3/h]\n")
        fichier_acq.write(current_time+";"+str(p_vent)+";"+str(P1.get_value(maq20_d,current_time))+","+str(section * sqrt(P2.get_value(maq20_d,current_time)*2/rho_air)*3600)+"\n")
        
        break
    
    sleep(1)
    count=count+1
   
    
   
###############################################################################
######################################################################
##############################################################################
print('#############   Paramètres initiaux   ################')

Ven.push_value(maq20_d, p_vent,current_time)
print('Pourcentage choisie des ventilateurs :', p_vent , '%')
print('debit d\'air :',str(section * sqrt(P2.get_value(maq20_d,current_time)*2/rho_air)*3600) , 'm^3/h')
print('Sur-pression obtenue dans le bâtiment :', P2.log_value[-1], 'Pa')


print('#####################################################')
print('#############   Début du protocole   ################')
print('#####################################################')



current_time=str(datetime.now())

#TODO premiere valeur : 0 pour débuter au début... ou alors une autre valeur
i=0




#fichier d'acquisition

nametime=str(datetime.now()).split(".")[0].replace("-", "_")
nametime=nametime.replace(":", "_")
name_file='Proto_surpression'+nametime+'.csv'
fichier_acq=open(name_file, 'w') #création d'un nouveau fichier seulement si celui-ci n'existe pas : sinon ERROR
fichier_acq.write("date_time;puissance ventilateur - [%];deltaP - [Pa];debit_air - [m^3/h]\n")
fichier_acq.close() 


# temps_pression=0
while i< 101:
    deltaP = []
    vit = []
    deb = []
    absolute_time = time.monotonic()
    compteur_ecriture=0 
    fichier_acq=open(name_file, 'a')   
    while compteur_ecriture<10 and i<101:
        t1 = time()
        i+=1
        try:
            current_time=str(datetime.now())
            while time.monotonic() - absolute_time < i*60 :
                deltaP.append(P1.get_value(maq20_d,current_time))
                deb.append(section * sqrt(P2.get_value(maq20_d,current_time)*2/rho_air))
                sleep(0.1)

            
            print("puissance du ventilateur " + str(p_vent))
            print("debit air " + str(sum(deb)/len(deb)))
            print("surpression " +str(sum(deltaP)/len(deltaP)))
            
            fichier_acq.write(current_time+";"+str(p_vent)+";"+str(sum(deb)/len(deb))+","+str(sum(deltaP)/len(deltaP))+"\n")
            deltaP = []
            vit = []
            deb = []

            compteur_ecriture+=1
            t2 = time()
            duree=t2-t1
            print('temps execution : ',duree)
            
        except:
            compteur_ecriture+=1
            print("Error Communication! Retrying soon...")
            sleep(45)
            
        
    fichier_acq.close() 
    p_vent += 10
    Ven.push_value(maq20_d, p_vent,current_time)
    #fermer le fichier régulièrement permet de donner accès aux valeurs dans le fichier
    #et ainsi pouvoir faire du post-traitement en cours de route
    

#Eteindre le ventilateur et la batterie chaude
Ven.push_value(maq20_d,0,"fin du protocole")

    
print('#####################################################')
print('#############   Fin du protocole   ################')
print('#####################################################')










