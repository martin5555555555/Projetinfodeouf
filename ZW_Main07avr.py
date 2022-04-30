# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 11:55:48 2022

@author: wangz (base on the code "QLxEC_Vendredi04.py")
"""

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
PBC_max=6000
print_it=3

maq20_d=None
Restart=True
nbofattempt=0


while(Restart and not(simulation)):
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
T_asp=[]
Pbat_th=[]
Pbat_r=[]
vit=[]
PBC_th=[]
PBC_r=[]


###############################################################################
###############################################################################

#initialisation
    
##############################################################################
#Boucle d'input/print

count=0;

while True :
    current_time=('init_'+str(count))
    
    #Réglage puissance réelle désirée
    PBC_th.append(float(input('Puissance Batterie Chaude theorique (PBC_th) injectée (W)')))
    pourcent=PBC_th[-1]/PBC_max
    print(pourcent)
    Bat.push_value(maq20_d, pourcent, current_time)
    
    #Puissance ventilateur
    pourcent_vent=float(input('Puissance ventilateur (%)'))/100
    Ven.push_value(maq20_d, pourcent_vent,current_time)
    # P_ventilateurs_choisie(P_vent_choisie)
    
    #Ouverture registre
    # registre_choix=float(input('Ouverture registre (%)'))
    # registre_choisi(registre_choix)
    
    
    #Affichage
       
    counter2=0
    
    for i in range (print_it):
        
        counter2=counter2+1
        current_time=(current_time+"."+str(counter2))
        
        wait=5
        print('Please wait for '+str(wait)+' second(s)')
        
        sleep(wait)
        
        
        vit.append(sqrt(P2.get_value(maq20_d,current_time)*2/rho_air))
        print("vit : "+str(vit[-1])+" m/s")
        P1.get_value(maq20_d,current_time)
        P1.print_value()
        
        T_asp.append((T1.get_value(maq20_d,current_time)+T2.get_value(maq20_d,current_time))/num_Tint)
        T1.print_value()
        T2.print_value()
        T3.get_value(maq20_d,current_time)
        T3.print_value()
        print("T_asp : "+str(T_asp[-1])+" °C")
        
        Tm.get_value(maq20_d,current_time)
        Ts.get_value(maq20_d,current_time)
        Tm.print_value()
        Ts.print_value()
        
        Pbat_th.append(PBC_th[-1]-cal_delta_P(rho_air, vit[-1], section, cp_air, T_asp[-1], Tm.log_value[-1]))
        print("Pbat_th : "+str(Pbat_th[-1])+" W")
        
        Pbat_r.append(cal_Pbat_r(rho_air, vit[-1], section, cp_air, T_asp[-1], Ts.log_value[-1]))
        print("Pbat_r : "+str(Pbat_r[-1])+" W")
        
        e=cal_ARD(Pbat_r[-1],Pbat_th[-1])
        print("Différence entre Pbat_r et Pbat_th est : "+str(e*100)+" %")
           
           

    choice=input('Ecrire "start" pour demarer le code :')
    
    if choice=='start':
        
        name_file='Initialiasation_Values_'+Ini_time+'.csv'
        fichier_acq=open(name_file, 'w')
        fichier_acq.write("date_time;P1 - [Pa];P2 - [Pa];Pbat - [W];T1 [°C];T2 [°C];T3 [°C];T_asp [°C];Tm [°C];Ts [°C];vitesse_air - [m/s];Pbat_r - [W]; Pbat_th - [W]\n")
        fichier_acq.write(str(T1.log_time)+";"+str(P1.log_value)+";"+str(P2.log_value)+";"+str(T1.log_value)+";"+str(T2.log_value)+";"+str(T3.log_value)+";"+str(T_asp)+";"+str(Tm.log_value)+";"+str(Ts.log_value)+";"+str(vit)+";"+str(Pbat_r)+";"+str(Pbat_th)+";\n")
        
        break
    
    sleep(1)
    count=count+1
   
    
   
###############################################################################
######################################################################
##############################################################################
print('#############   Paramètres initiaux   ################')

print('Pourcentage choisie des ventilateurs :', pourcent*100 , '%')
print('Vitesse de l\'air :', vit[-1], 'm/s')
print('Sur-pression obtenue dans le bâtiment :', P2.log_value[-1], 'Pa')
print('Puissance réelle désirée :', Pbat_th[-1], 'W')
print('Puissance des batteries chaudes correspondant :', PBC_th, 'W')
print('Puissance réelle injectée :', Pbat_r[-1], 'W')

print('#####################################################')
print('#############   Début du protocole   ################')
print('#####################################################')

#Efface tous les enregistrement dans la phase d'initialisation 
# (pas nécessaire, juste pour que tous les value intéressée sont de la même longueur)
        
# P1.clear()
# P2.clear()
# T1.clear()
# T2.clear()
        

#sollicitaion_P est définie dans mapV2.py
l=len(sollicitation_P)
#list_test=crea_list(1000,0)
#sollicitation_P=list_test

#Grandeurs d'intérêt

current_time=str(datetime.now())

vit.append(sqrt(P2.get_value(maq20_d,current_time)*2/rho_air))
P1.get_value(maq20_d,current_time)

T_asp.append((T1.get_value(maq20_d,current_time)+T2.get_value(maq20_d,current_time))/num_Tint)
T3.get_value(maq20_d,current_time)
Tm.get_value(maq20_d,current_time)
Ts.get_value(maq20_d,current_time)

F1.get_value(maq20_d,current_time)
F2.get_value(maq20_d,current_time)
F3.get_value(maq20_d,current_time)
F4.get_value(maq20_d,current_time)
F5.get_value(maq20_d,current_time)
F6.get_value(maq20_d,current_time)
F7.get_value(maq20_d,current_time)
F8.get_value(maq20_d,current_time)

PyrA.get_value(maq20_d,current_time)
PyrB.get_value(maq20_d,current_time)

print_all()

#TODO premiere valeur : 0 pour débuter au début... ou alors une autre valeur
i=300

Pbat_th.append(sollicitation_P[i]*2/3)
print("Pbat_th : "+str(Pbat_th[-1])+" W")

PBC_th.append(Pbat_th[-1]+cal_delta_P(rho_air, vit[-1], section, cp_air, T_asp[-1], Tm.log_value[-1]))
pourcent=PBC_th[-1]/PBC_max
Bat.push_value(maq20_d, pourcent, current_time)
print("PBC_th : "+str(PBC_th[-1])+" W")
        
Pbat_r.append(cal_Pbat_r(rho_air, vit[-1], section, cp_air, T_asp[-1], Ts.log_value[-1]))
print("Pbat_r : "+str(Pbat_r[-1])+" W")

PBC_r.append(cal_PBC_r(rho_air, vit[-1], section, cp_air, Tm.log_value[-1], Ts.log_value[-1]))
print("PBC_r : "+str(PBC_r[-1])+" W")

e_bat=cal_ARD(Pbat_r[-1],Pbat_th[-1])
print("Différence entre Pbat_r et Pbat_th est : "+str(e_bat*100)+" %")
        
e_BC=cal_ARD(PBC_r[-1],PBC_th[-1])
print("Différence entre PBC_r et PBC_th est : "+str(e_BC*100)+" %")

#fichier d'acquisition

nametime=str(datetime.now()).split(".")[0].replace("-", "_")
nametime=nametime.replace(":", "_")
name_file='ProtoZW_test2'+nametime+'.csv'
fichier_acq=open(name_file, 'w') #création d'un nouveau fichier seulement si celui-ci n'existe pas : sinon ERROR
#TODO adapter la premiere ligne a chaque experience
fichier_acq.write("date;Pconsigne(Pbat_th) - [W];Pbat_r - [W];PBC_th - [W];PBC_r - [W];vitesse_air - [m/s];sur-pression - [Pa];T1;T2;T3;T_asp;Ts;Tm;pyranoA;pyranoB;flux 9;flux 4;flux 2;flux 1;flux 6;flux 3;flux 5;flux 3small\n")
fichier_acq.write(current_time+";"+str(Pbat_th[-1])+";"+str(Pbat_r[-1])+";"+str(PBC_th[-1])+";"+str(PBC_r[-1])+";"+str(vit[-1])+";"+str(P1.log_value[-1])+";"+str(T1.log_value[-1])+";"+str(T2.log_value[-1])+";"+str(T3.log_value[-1])+";"+str(T_asp[-1])+";"+str(Ts.log_value[-1])+";"+str(Tm.log_value[-1])+";"+str(PyrA.log_value[-1])+";"+str(PyrB.log_value[-1])+";"+str(F1.log_value[-1])+";"+str(F2.log_value[-1])+";"+str(F3.log_value[-1])+";"+str(F4.log_value[-1])+";"+str(F5.log_value[-1])+";"+str(F6.log_value[-1])+";"+str(F7.log_value[-1])+";"+str(F8.log_value[-1])+"\n")
fichier_acq.close()


# temps_pression=0
while i<(l):
    compteur_ecriture=0 #pour voir tous les combien de ligne on ferme le fichier et on le rouvre
    fichier_acq=open(name_file, 'a')   #ouverture en mode "append"
    while compteur_ecriture<5 and i<(l):
        t1 = time()
        i+=1
        try:
            current_time=str(datetime.now())
            
            ##sécurité avant la pause
            if pourcent_vent==0 or vit[-1]<0.05 :   #sécurité vis à vis de la ventilation : il faut qu'il y ait une circulation d'air pour allumer les BC
    
                fichier_acq.write(current_time+";ERROR - SAFETY : P_BC = 0"+"\n")
                print('ERROR VENTILATION')
                pourcent=0
                Bat.push_value(maq20_d,pourcent,current_time) #mise à 0 de PBC
                
            ###################################################b
            sleep(59.5) #régler le temps d'attente entre chaque itération
            #ATTENTION durant ce temps d'attente, aucune sécurité ne sera vérifier !!! Sinon il faut changer la manière d'écrire le programme
            ###################################################
            
            #calculer PBC
            print(' ')
            print('Target step '+str(i)+'/'+str(l)+' : '+str(Pbat_th[-1])+' W')
            PBC_r.append(cal_PBC_r(rho_air, vit[-1], section, cp_air, Tm.log_value[-1], Ts.log_value[-1]))
            print('Puissance batterie chaude réelle: '+str(PBC_r[-1])+' W')
            ##sécurité après la pause (à voir si vraiment utile - temps d'exécution entre 2 pauses assez court)
            if pourcent_vent==0 or vit[-1]<0.05 :   #sécurité vis à vis de la ventilation : il faut qu'il y ait une circulation d'air pour allumer les BC
    
                fichier_acq.write("ERROR - SAFETY : P_BC = 0"+"\n")
                print('ERROR VENTILATION')
                pourcent=0
                Bat.push_value(maq20_d,pourcent,current_time) #mise à 0 de PBC
                #Il faudrait voir pour réimposer une vitesse d'air... sinon cela ne repartira pas !! Mais quelle vitesse ?
               
            
            #aqcuérir toutes les grandeurs nécessaires
            #TODO ajouter toutes les températures et tous les flux
            current_time=str(datetime.now())
    
            vit.append(sqrt(P2.get_value(maq20_d,current_time)*2/rho_air))
            P1.get_value(maq20_d,current_time)
    
            T_asp.append((T1.get_value(maq20_d,current_time)+T2.get_value(maq20_d,current_time))/num_Tint)
            Tm.get_value(maq20_d,current_time)
            Ts.get_value(maq20_d,current_time)
            T3.get_value(maq20_d,current_time)
    
            F1.get_value(maq20_d,current_time)
            F2.get_value(maq20_d,current_time)
            F3.get_value(maq20_d,current_time)
            F4.get_value(maq20_d,current_time)
            F5.get_value(maq20_d,current_time)
            F6.get_value(maq20_d,current_time)
            F7.get_value(maq20_d,current_time)
            F8.get_value(maq20_d,current_time)
    
            PyrA.get_value(maq20_d,current_time)
            PyrB.get_value(maq20_d,current_time)
            
            print_all()
            
            Pbat_th.append(sollicitation_P[i]*2/3) #TODO coeff de modif consigne
    
            PBC_th.append(Pbat_th[-1]+cal_delta_P(rho_air, vit[-1], section, cp_air, T_asp[-1], Tm.log_value[-1]))
            
            if Ts.log_value[-1]>50:
                pourcent=0
                print('WARNING TEMPERATURE : hot batteries set to 0 W') 
            else:
                pourcent=PBC_th[-1]/PBC_max
            Bat.push_value(maq20_d, pourcent, current_time)
            
            Pbat_r.append(cal_Pbat_r(rho_air, vit[-1], section, cp_air, T_asp[-1], Ts.log_value[-1]))
    
            PBC_r.append(cal_PBC_r(rho_air, vit[-1], section, cp_air, Tm.log_value[-1], Ts.log_value[-1]))
    
            e_bat=cal_ARD(Pbat_r[-1],Pbat_th[-1])
            print("Pbat_r : ", Pbat_r[-1])
            print("Pbat_th : ", Pbat_th[-1])
            print("Différence entre Pbat_r et Pbat_th est : "+str(e_bat*100)+" %")
            
            e_BC=cal_ARD(PBC_r[-1],PBC_th[-1])
            print("PBC_r : ", PBC_r[-1])
            print("PBC_th : ", PBC_th[-1])
            print("Différence entre PBC_r et PBC_th est : "+str(e_BC*100)+" %")
    

            #enregistrer tout ce que l'on veut dans le fichier csv
            #TODO adapter cette ligne a chaque experimentation
            fichier_acq.write(current_time+";"+str(Pbat_th[-1])+";"+str(Pbat_r[-1])+";"+str(PBC_th[-1])+";"+str(PBC_r[-1])+";"+str(vit[-1])+";"+str(P1.log_value[-1])+";"+str(T1.log_value[-1])+";"+str(T2.log_value[-1])+";"+str(T3.log_value[-1])+";"+str(T_asp[-1])+";"+str(Ts.log_value[-1])+";"+str(Tm.log_value[-1])+";"+str(PyrA.log_value[-1])+";"+str(PyrB.log_value[-1])+";"+str(F1.log_value[-1])+";"+str(F2.log_value[-1])+";"+str(F3.log_value[-1])+";"+str(F4.log_value[-1])+";"+str(F5.log_value[-1])+";"+str(F6.log_value[-1])+";"+str(F7.log_value[-1])+";"+str(F8.log_value[-1])+"\n")
            
            compteur_ecriture+=1
            t2 = time()
            duree=t2-t1
            print('temps execution : ',duree)
            
        except:
            compteur_ecriture+=1
            print("Error Communication! Retrying soon...")
            sleep(45)
            
        
    fichier_acq.close() 
    #fermer le fichier régulièrement permet de donner accès aux valeurs dans le fichier
    #et ainsi pouvoir faire du post-traitement en cours de route
    

#Eteindre le ventilateur et la batterie chaude
Bat.push_value(maq20_d,0,"fin du protocole")
sleep(180)
Ven.push_value(maq20_d,0,"fin du protocole")

    
print('#####################################################')
print('#############   Fin du protocole   ################')
print('#####################################################')










