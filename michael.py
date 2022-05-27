# -*- coding: utf-8 -*-
"""
Created on Fri May 27 10:45:04 2022

@author: marie
"""
# from mapV2 import *
from ProtoV2 import *
from maq20 import MAQ20

import time as Time
from time import time
from datetime import datetime
from math import *
#je prends la consigne de Morgane (pas de temps de temps de 1minute, durée = 4 jours)
from consigneBureauFred import *



class Context:
    def __init__(self, is_simulation):
        self._name = "Name + date etc?..."
        self._is_simulation = is_simulation
        
        self._Tint1=Temp_PT100(name = "Tint1", channel = 3, is_simulation = self._is_simulation,module="S0153011-07")
        #T2
        #T2=Temp_PT100(name = "T2", channel = 2, Tmin = 0, Tmax = 100)
        self._Tint2=Temp_PT100(name = "Tint2", channel = 4, is_simulation = self._is_simulation,module="S0153011-07")
        self._Tint3=Temp_PT100(name = "Tint3", channel = 3, is_simulation = self._is_simulation,module="S0153011-08")
        #self._T4=Temp_PT100(name = "T4", channel = 0, is_simulation = self._is_simulation,module="S0153011-07")
        
        self._Tbe1=Temp_PT100(name = "Tbe1", channel = 0, is_simulation = self._is_simulation,module="S0153011-08")
        self._Tbe2=Temp_PT100(name = "Tbe2", channel = 1, is_simulation = self._is_simulation,module="S0153011-08")
        self._Tbe3=Temp_PT100(name = "Tbe3", channel = 2, is_simulation = self._is_simulation,module="S0153011-08")
        
        self._Tbs1=Temp_PT100(name = "Tbs1", channel = 0, is_simulation = self._is_simulation,module="S0153011-07")
        self._Tbs2=Temp_PT100(name = "Tbs2", channel = 1, is_simulation = self._is_simulation,module="S0153011-07")
        self._Tbs3=Temp_PT100(name = "Tbs3", channel = 2, is_simulation = self._is_simulation,module="S0153011-07")
        
        #On the machine

        #T_soufflage
        self._Ts=Temp_PT100(name = "T_soufflage", channel = 4, is_simulation = self._is_simulation,module="S0153011-08")
        #T_melange
        #self._Tm=Temp_PT100(name = "T_melange", channel = 4, is_simulation = self._is_simulation,module="S0153011-08")

        #######Fluxmeter####### 
        self._F6=Fluxmeter(name = "Fluxmeter_6", channel = 0, rate = 132/1000000, is_simulation = self._is_simulation)
        self._F2=Fluxmeter(name = "Fluxmeter_2", channel = 1, rate = 269/1000000, is_simulation = self._is_simulation)        
        self._F3=Fluxmeter(name = "Fluxmeter_3", channel = 2, rate = 284/1000000, is_simulation = self._is_simulation)
        
        #######Capteur de pression#######

        #P1
        self._p1=Cap_pression(name = "p_debit", channel = 0, Vmin = 0, Vmax = 10, Pmin = 0, Pmax = 500, is_simulation = self._is_simulation)

        #P2
        # self._P2=Cap_pression(name = "p_intext", channel = 1, Vmin = 0, Vmax = 10, Pmin = 0, Pmax = 500, is_simulation = self._is_simulation)

        #######Controle#######

        #Ventilateur
        self._Vent=Controle(name = "Controle_Vent", channel = 1, Vmin = 0, Vmax = 10, is_simulation = self._is_simulation)

        #Batterie Chaude
        self._BC=Controle(name = "Control_BC",    channel = 4, Vmin = 0, Vmax = 10, is_simulation = self._is_simulation)

        #######Pyranometer#######

        #Pyrano
        self._PyrA=Pyrano(name = "PyranoA", channel = 0, is_simulation = self._is_simulation)

        #PyranoB
        self._PyrB=Pyrano(name = "PyranoB", channel = 1, is_simulation = self._is_simulation)

        #PyranoC
        self._PyrC=Pyrano(name = "PyranoC", channel = 2, is_simulation = self._is_simulation)
        
        #Contrôle de Pbat_th
        # from consigne_test import *

        self._sollicitation_P= consigne_PBC#[5 for i in range (60*24*5+5)]#consigne_PBC #consigne de contrôle de P_réelle (format à voir)

        #...
        
        #mettre toutes les valeusr de mapV2 ici

        #ToDO: entrer tous les Instruments pressions initialement à la valeur none, et aussi les consignes et les puissances
        self._Ini_time = str(datetime.now()).split(",")[0].replace("-", "_")
        self._Ini_time = self._Ini_time.replace(":", "_")
        self._T_asp = []
        # self._Pbat_th = []
        # self._Pbat_r = []
        self._Pint_th = []
        self._Pint_r = []
        self._Tbe = []
        
        self._vit = []
        self._PBC_th = []
        self._PBC_r = []
        self._diameter=0.315 #TODO indiquer la bonne valeur
        self._section = 1*pi*(self._diameter/2)**2 #0.8165
        self._cp_air = 1005 #TODO indiquer la bonne valeur
        self._rho_air = 1.29  #TODO indiquer la bonne valeur 
        self._PBC_max=9000
        self._maq20_d=None
        self._num_Tint = 3 # nbr de PT100 àl'intérieur du batiment 
        self._num_Tbe = 3 # nbr de PT100 à l'aspiration de la batterie chaude
        self._pourcent = None
        self._pourcent_vent = None


    # def cal_delta_P(self):
    #     dP=self._rho_air* self._vit[-1]*self._section*self._cp_air*(self._T_asp[-1]-self._Tm.log_value[-1])
    #     return dP

    def cal_Pint_r(self): 
        #calculer Pbatiment,reelle
        Pint_r=self._rho_air*self._vit[-1]*self._section*self._cp_air*(self._Ts.log_value[-1]-self._T_asp[-1])
        return Pint_r

    def cal_PBC_r(self):
        PBC_r=self._rho_air*self._vit[-1]*self._section*self._cp_air*(self._Ts.log_value[-1]-self._Tbe[-1])
        return PBC_r

    def cal_ARD(self, reelle, theorie):
        #calculate the absolute relative deviation
        if(theorie==0 or (reelle-theorie)==0):
            print("error cal_ARD : reelle "+str(reelle)+", theorie "+str(theorie))
            return 0
        ARD=abs((reelle-theorie)/theorie)
        return ARD
    def print_all(self):
        self._Tint1.print_value()
        self._Tint2.print_value()
        self._Tint3.print_value()
        self._Tbe1.print_value()
        self._Tbe2.print_value()
        self._Tbe3.print_value()
        self._Tbs1.print_value()
        self._Tbs2.print_value()
        self._Tbs3.print_value()
        # self._T4.print_value()
        # self._Tm.print_value()
        self._Ts.print_value()
        
        self._p1.print_value()
        #self._vit.print_value()
        # self._P2.print_value()
        
        self._Vent.print_value()
        self._BC.print_value()
        
        # #self._F1.print_value()
        self._F2.print_value()
        self._F3.print_value()
        # #self._F4.print_value()
        # self._F5.print_value()
        self._F6.print_value()
        # #self._F7.print_value()
        #self._F8.print_value()
        
        self._PyrA.print_value()
        self._PyrB.print_value()
        self._PyrC.print_value()
    

class General_State():
    def __init__(self, is_simulation):
        self._is_simulation = is_simulation

    def run_from(self, state, context):
        while state is not None:
            state = state.run(context)

class State_connect(General_State):
    def __init__(self, is_simulation):
        super().__init__(is_simulation)

    def run(self, context):
        nbofattempt=0
        Restart = True
        #connection
        
        print("pre attempting connection")
        while(Restart and not(self._is_simulation)):
            try:
                print("attempting connection")
                context._maq20_d = MAQ20(ip_address="192.168.128.100", port=502)
                print("connection ok")
                print(context._maq20_d)
                Restart=False
            except:
                Restart=True
                print("Error connection... Trying again")
                sleep(0.1)
                nbofattempt+=1
                if(nbofattempt>20):
                    print("Timeout : too many unsuccessfull attempts")
                    raise ValueError

        print("connection success")

class State_init(General_State):
    def __init__(self, is_simulation):
        super().__init__(is_simulation)

    def run(self, context):

        
        count = 0
        
           
        current_time=('init_'+str(count))
    
        #Réglage puissance réelle désirée
        input_Pint_th = float(input('Puissance batiment interieur emise (W)'))
        context._PBC_th.append(input_Pint_th)
        context._pourcent=context._PBC_th[-1]/context._PBC_max
        print(context._pourcent)
        context._BC.push_value(context._maq20_d, context._pourcent, current_time)
        
        #Puissance ventilateur
        context._pourcent_vent=float(input('Puissance ventilateur (%)'))/100
        context._Vent.push_value(context._maq20_d, context._pourcent_vent,current_time)

        counter2=0
        print_it =  3
        for i in range (print_it):
            counter2 += 1
            context._current_time=(current_time+"."+str(counter2))
                
            wait= 0
            print('Please wait for '+str(wait)+' second(s)')
            # print(P2.log_value)
            sleep(wait)
                
             
            context._vit.append(sqrt(context._p1.get_value(context._maq20_d,current_time)*2/context._rho_air))
            print("vit : "+str(context._vit[-1])+" m/s")
            context._p1.get_value(context._maq20_d,current_time)
            context._p1.print_value()
            
            # acquisition des températures intérieures 
            context._Tint1.get_value(context._maq20_d,current_time)
            context._Tint2.get_value(context._maq20_d,current_time)
            context._Tint3.get_value(context._maq20_d,current_time)            
            context._Tint1.print_value()
            context._Tint2.print_value()
            context._Tint3.print_value()
            
            # acquisition des températures de l'entree de la batterie 
            context._Tbe1.get_value(context._maq20_d,current_time)
            context._Tbe2.get_value(context._maq20_d,current_time)
            context._Tbe3.get_value(context._maq20_d,current_time)            
            context._Tbe1.print_value()
            context._Tbe2.print_value()
            context._Tbe3.print_value()
            
            # acquisition des températures de la sortie de la batterie 
            context._Tbs1.get_value(context._maq20_d,current_time)
            context._Tbs2.get_value(context._maq20_d,current_time)
            context._Tbs3.get_value(context._maq20_d,current_time)            
            context._Tbs1.print_value()
            context._Tbs2.print_value()
            context._Tbs3.print_value()
            
            # calcul de la température moyenne de l'entree batterie chaude
            context._Tbe.append((context._Tbe1.log_value[-1] + 
                                 context._Tbe2.log_value[-1] + 
                                 context._Tbe3.log_value[-1])/context._num_Tbe)
            # température moyenne de l'entree batterie chaude
            print("T_be : "+str(context._Tbe[-1])+" °C")            
            
            # calcul de la température intérieure moyenne 
            context._T_asp.append((context._Tint1.log_value[-1] + context._Tint2.log_value[-1] + context._Tint3.log_value[-1] +
                                   context._Tbe1.log_value[-1] + context._Tbe2.log_value[-1] + context._Tbe3.log_value[-1])/(context._num_Tint+context._num_Tbe))
            # temperature de l'interieur
            print("T_asp : "+str(context._T_asp[-1])+" °C")

        

            
            # context._T3.get_value(context._maq20_d,current_time)
            # context._T3.print_value()
            # context._T4.get_value(context._maq20_d,current_time)
            # context._T4.print_value()
                
            # context._Tm.get_value(context._maq20_d,current_time)
            context._Ts.get_value(context._maq20_d,current_time)
            # context._Tm.print_value()
            context._Ts.print_value()
                    
            context._Pint_th.append(context._PBC_th[-1])
            print("Pint_th : "+str(context._Pint_th[-1])+" W")
                    
            context._Pint_r.append(context.cal_Pint_r())
            print("Pint_r : "+str(context._Pint_r[-1])+" W")
                    
            e = cal_ARD(context._Pint_r[-1],context._Pint_th[-1])
            print("Différence entre Pint_r et Pint_th est : "+str(e*100)+" %")

            
   
        
class State_run(General_State):
    def __init__(self, is_simulation):
        super().__init__(is_simulation)

    def run(self, context):
        name_file='Initialiasation_Values_'+context._Ini_time+'.csv'
        fichier_acq=open(name_file, 'w')
        fichier_acq.write("date_time;p1 - [Pa];Tint1 [°C];Tint2 [°C];Tint3 [°C];Tbe1 [°C];Tbe2 [°C];Tbe3 [°C];Tbs1 [°C];Tbs2 [°C];Tbs3 [°C];T_asp [°C];Ts [°C];vitesse_air - [m/s];Pint_r - [W]; Pint_th - [W]\n")
        fichier_acq.write(str(context._Tint1.log_time)+";"+
                          str(context._p1.log_value)+";"+
                          # str(context._P2.log_value)+";"+
                          str(context._Tint1.log_value)+";"+
                          str(context._Tint2.log_value)+";"+
                          str(context._Tint3.log_value)+";"+
                          str(context._Tbe1.log_value)+";"+
                          str(context._Tbe2.log_value)+";"+
                          str(context._Tbe3.log_value)+";"+
                          str(context._Tbs1.log_value)+";"+
                          str(context._Tbs2.log_value)+";"+
                          str(context._Tbs3.log_value)+";"+
                          str(context._T_asp)+";"+
                          # str(Tm.log_value)+";"+
                          str(context._Ts.log_value)+";"+
                          str(context._vit)+";"+
                          str(context._Pint_r)+";"+
                          str(context._Pint_th)+";\n")
        
        
        count = 0
        sleep(1)
        count=count+1
        ###############################################################################
        ######################################################################
        ##############################################################################
        print('#############   Paramètres initiaux   ################')
        # print(P2.log_value)

        print('Pourcentage choisie des ventilateurs :', context._pourcent*100 , '%')
        print('Vitesse de l\'air :', context._vit[-1], 'm/s')
        # print('Sur-pression obtenue dans le bâtiment :', context._P2.log_value[-1], 'Pa')
        print('Puissance réelle désirée :', context._Pint_th[-1], 'W')
        print('Puissance des batteries chaudes correspondant :', context._PBC_th, 'W')
        print('Puissance réelle injectée :', context._Pint_r[-1], 'W')

        print('#####################################################')
        print('#############   Début du protocole   ################')
        print('#####################################################')
        current_time=str(datetime.now())

        context._vit.append(sqrt(context._p1.get_value(context._maq20_d,current_time)*2/context._rho_air))
        context._p1.get_value(context._maq20_d,current_time)

        context._T_asp.append((context._Tint1.get_value(context._maq20_d,current_time)+
                               context._Tint2.get_value(context._maq20_d,current_time)+
                               context._Tint3.get_value(context._maq20_d,current_time)+
                               context._Tbe1.get_value(context._maq20_d,current_time)+
                               context._Tbe2.get_value(context._maq20_d,current_time)+
                               context._Tbe3.get_value(context._maq20_d,current_time))/(context._num_Tint+context._num_Tbe))
        context._Tint3.get_value(context._maq20_d,current_time)
        # context._T4.get_value(context._maq20_d,current_time)
        # context._Tm.get_value(context._maq20_d,current_time)
        context._Ts.get_value(context._maq20_d,current_time)
        # context._F1.get_value(context._maq20_d,current_time)
        context._F2.get_value(context._maq20_d,current_time)
        context._F3.get_value(context._maq20_d,current_time)#
        # context._F4.get_value(context._maq20_d,current_time)
        # context._F5.get_value(context._maq20_d,current_time)
        context._F6.get_value(context._maq20_d,current_time)#
        # context._F7.get_value(context._maq20_d,current_time)
        # context._F8.get_value(context._maq20_d,current_time)
        context._PyrA.get_value(context._maq20_d,current_time)
        context._PyrB.get_value(context._maq20_d,current_time)
        context._PyrC.get_value(context._maq20_d,current_time)

        context.print_all()

        #TODO premiere valeur : 0 pour débuter au début... ou alors une autre valeur
        i=2772

        context._Pint_th.append(context._sollicitation_P[i])
        print("Pint_th : "+str(context._Pint_th[-1])+" W")

        context._PBC_th.append(context._Pint_th[-1])
        pourcent=context._PBC_th[-1]/context._PBC_max
        context._BC.push_value(context._maq20_d, pourcent, current_time)
        print("PBC_th : "+str(context._PBC_th[-1])+" W")
        
        
        context._Pint_r.append(context.cal_Pint_r())
        print("Pint_r : "+str(context._Pint_r[-1])+" W")

        context._PBC_r.append(context.cal_PBC_r())
        print("PBC_r : "+str(context._PBC_r[-1])+" W")

        e_bat=context.cal_ARD(context._Pint_r[-1],context._Pint_th[-1])
        print("Différence entre Pint_r et Pint_th est : "+str(e_bat*100)+" %")
                
        e_BC=context.cal_ARD(context._PBC_r[-1],context._PBC_th[-1])
        print("Différence entre PBC_r et PBC_th est : "+str(e_BC*100)+" %")

        #fichier d'acquisition

        nametime=str(datetime.now()).split(".")[0].replace("-", "_")
        nametime=nametime.replace(":", "_")
        name_file='ProtoZW_test2'+nametime+'.csv'
        fichier_acq=open(name_file, 'w') #création d'un nouveau fichier seulement si celui-ci n'existe pas : sinon ERROR
        #TODO adapter la premiere ligne a chaque experience
        fichier_acq.write("date;Pconsigne(Pint_th) - [W];Pint_r - [W];PBC_th - [W];PBC_r - [W];vitesse_air - [m/s];sur-pression - [Pa];Tint1;Tint2;Tint3;Tbe1;Tbe2;Tbe3;Tbs1;Tbs2;Tbs3;T_asp;Ts;pyranoA;pyranoB;pyranoC;F2; F3; F6; flux 9;flux 2;flux 2;flux 3;flux 4;flux 5;flux 6;flux 7\n")
        fichier_acq.write(current_time+";"+
                          str(context._Pint_th[-1])+";"+
                          str(context._Pint_r[-1])+";"+
                          str(context._PBC_th[-1])+";"+
                          str(context._PBC_r[-1])+";"+
                          str(context._vit[-1])+";"+
                          str(context._p1.log_value[-1])+";"+
                          str(context._Tint1.log_value[-1])+";"+
                          str(context._Tint2.log_value[-1])+";"+
                          str(context._Tint3.log_value[-1])+";"+
                          str(context._Tbe1.log_value[-1])+";"+
                          str(context._Tbe2.log_value[-1])+";"+
                          str(context._Tbe3.log_value[-1])+";"+
                          str(context._Tbs1.log_value[-1])+";"+
                          str(context._Tbs2.log_value[-1])+";"+
                          str(context._Tbs3.log_value[-1])+";"+
                          str(context._T_asp[-1])+";"+
                          str(context._Ts.log_value[-1])+";"+
                          # str(context._Tm.log_value[-1])+";"+
                          str(context._PyrA.log_value[-1])+";"+
                          str(context._PyrB.log_value[-1])+";"+
                          str(context._PyrC.log_value[-1])+";"+
                          # str(context._F1.log_value[-1])+";"+
                           str(context._F2.log_value[-1])+";"+
                           str(context._F3.log_value[-1])+";"+
                          # str(context._F4.log_value[-1])+";"+
                          # str(context._F5.log_value[-1])+";"+
                           str(context._F6.log_value[-1])+";"+
                          # str(context._F7.log_value[-1])+";"+
                          # str(context._F8.log_value[-1])+
                          "\n")
        fichier_acq.close()

        l=len(context._sollicitation_P)

        # temps_pression=0
        while i<(l):
            context._Pint_r_ms =[]
            context._PBC_r_ms =[]
            context._vit_ms =[]
            context._p1_ms = []
            context._Ts_ms = []
            context._Tint1_ms = []
            context._Tint2_ms = []
            context._Tint3_ms = []
            context._Tbe1_ms = []
            context._Tbe2_ms = []
            context._Tbe3_ms = []
            context._Tbs1_ms = []
            context._Tbs2_ms = []
            context._Tbs3_ms = []
            context._F2_ms = []
            context._F3_ms = []
            context._F6_ms = []
            context._PyrA_ms = []
            context._PyrB_ms = []
            context._PyrC_ms = []
            
            context._Pint_r_moy =[]
            context._PBC_r_moy =[]
            context._vit_moy =[]
            context._p1_moy = []
            context._Ts_moy = []
            context._Tint1_moy = []
            context._Tint2_moy = []
            context._Tint3_moy = []
            context._Tbe1_moy = []
            context._Tbe2_moy = []
            context._Tbe3_moy = []
            context._Tbs1_moy = []
            context._Tbs2_moy = []
            context._Tbs3_moy = []
            context._Tasp_moy = []
            context._F2_moy = []
            context._F3_moy = []
            context._F6_moy = []
            context._PyrA_moy = []
            context._PyrB_moy = []
            context._PyrC_moy = []
            context._Tbe_moy = []
            
            
            absolute_time = Time.monotonic()
            compteur_ecriture=0 #pour voir tous les combien de ligne on ferme le fichier et on le rouvre
            fichier_acq=open(name_file, 'a')   #ouverture en mode "append"


            t1 = time()
            try:
                current_time=str(datetime.now())
                
                
                context._Pint_th.append(context._sollicitation_P[i]) #TODO coeff de modif consigne
                
                ##sécurité avant la pause
                if context._pourcent_vent==0 or context._vit[-1]<0.05 :   #sécurité vis à vis de la ventilation : il faut qu'il y ait une circulation d'air pour allumer les BC
        
                    fichier_acq.write(current_time+";ERROR - SAFETY : P_BC = 0"+"\n")
                    print('ERROR VENTILATION')
                    pourcent=0
                    context._BC.push_value(context._maq20_d,pourcent,current_time) #mise à 0 de PBC
                    
                
                #calculer PBC
                print(' ')
                print('Target step '+str(i)+'/'+str(l)+' : '+str(context._Pint_th[-1])+' W')
                # print("Consigne : "+str(context._sollicitation_P[i])+' W')
                # context._PBC_r.append(context.cal_PBC_r())
                # print('Puissance batterie chaude réelle: '+str(context._PBC_r[-1])+' W')
                ##sécurité après la pause (à voir si vraiment utile - temps d'exécution entre 2 pauses assez court)
                print('Air speed : '+str(context._vit[-1]))
                if context._pourcent_vent==0 or context._vit[-1]<0.05 :   #sécurité vis à vis de la ventilation : il faut qu'il y ait une circulation d'air pour allumer les BC
        
                    fichier_acq.write("ERROR - SAFETY : P_BC = 0"+"\n")
                    print('ERROR VENTILATION')
                    pourcent=0
                    context._BC.push_value(context._maq20_d,pourcent,current_time) #mise à 0 de PBC
                    #Il faudrait voir pour réimposer une vitesse d'air... sinon cela ne repartira pas !! Mais quelle vitesse ?
                
                
                sleep(1)

                
                print("acquisition + averaging")      
                
              # echantillonage pour moyennisation 
                while ((Time.monotonic() - absolute_time) < 55) : #TODO needs to be 60
                    context._BC.push_value(context._maq20_d, 1, current_time)
                    current_time=str(datetime.now())
                    context._p1_ms.append(context._p1.get_value(context._maq20_d,current_time))
                    # context._P2_moy.append(context._P2.get_value(context._maq20_d,current_time))
                    # context._Tm_moy.append(context._Tm.get_value(context._maq20_d,current_time))
                    context._Ts_ms.append(context._Ts.get_value(context._maq20_d,current_time))
                    context._Tint1_ms.append(context._Tint1.get_value(context._maq20_d,current_time))
                    context._Tint2_ms.append(context._Tint2.get_value(context._maq20_d,current_time))
                    context._Tint3_ms.append(context._Tint3.get_value(context._maq20_d,current_time))
                    context._Tbe1_ms.append(context._Tbe1.get_value(context._maq20_d,current_time))
                    context._Tbe2_ms.append(context._Tbe2.get_value(context._maq20_d,current_time))
                    context._Tbe3_ms.append(context._Tbe3.get_value(context._maq20_d,current_time))
                    context._Tbs1_ms.append(context._Tbs1.get_value(context._maq20_d,current_time))
                    context._Tbs2_ms.append(context._Tbs2.get_value(context._maq20_d,current_time))
                    context._Tbs3_ms.append(context._Tbs3.get_value(context._maq20_d,current_time))
                    # context._T4_moy.append(context._T4.get_value(context._maq20_d,current_time))
            
                    # context._F1_moy.append(context._F1.get_value(context._maq20_d,current_time))
                    context._F2_ms.append(context._F2.get_value(context._maq20_d,current_time))
                    context._F3_ms.append(context._F3.get_value(context._maq20_d,current_time))
                    # context._F4_moy.append(context._F4.get_value(context._maq20_d,current_time))
                    # context._F5_moy.append(context._F5.get_value(context._maq20_d,current_time))
                    context._F6_ms.append(context._F6.get_value(context._maq20_d,current_time))
                    # context._F7_moy.append(context._F7.get_value(context._maq20_d,current_time))
                    # context._F8_moy.append(context._F8.get_value(context._maq20_d,current_time))
        
                    context._PyrA_ms.append(context._PyrA.get_value(context._maq20_d,current_time))
                    context._PyrB_ms.append(context._PyrB.get_value(context._maq20_d,current_time))
                    context._PyrC_ms.append(context._PyrC.get_value(context._maq20_d,current_time))
                    
                    sleep(0.1)
                # calcul des moyennes 
                # print(str(context._Tbs3_ms))
                context._Tint1_moy.append(sum(context._Tint1_ms)/len(context._Tint1_ms))
                context._Tint2_moy.append(sum(context._Tint2_ms)/len(context._Tint2_ms))
                # context._vit_moy.append(sqrt((sum( context._p1_moy)/len( context._p1_moy))*2/ context._rho_air))
         
                context._Tint2_moy.append(sum(context._Tint2_ms)/len(context._Tint2_ms))
                context._Tint3_moy.append(sum(context._Tint3_ms)/len(context._Tint3_ms))
                context._Tbe1_moy.append(sum(context._Tbe1_ms)/len(context._Tbe1_ms))
                context._Tbe2_moy.append(sum(context._Tbe2_ms)/len(context._Tbe2_ms))
                context._Tbe3_moy.append(sum(context._Tbe3_ms)/len(context._Tbe3_ms))
                context._Tbs1_moy.append(sum(context._Tbs1_ms)/len(context._Tbs1_ms))
                context._Tbs2_moy.append(sum(context._Tbs2_ms)/len(context._Tbs2_ms))
                context._Tbs3_moy.append(sum(context._Tbs3_ms)/len(context._Tbs3_ms))
                context._Ts_moy.append(sum(context._Ts_ms)/len(context._Ts_ms))
                context._p1_moy.append(sum( context._p1_ms)/len( context._p1_ms))
                context._F2_moy.append(sum( context._F2_ms)/len( context._F2_ms))
                context._F3_moy.append(sum( context._F3_ms)/len( context._F3_ms))
                context._F6_moy.append(sum( context._F6_ms)/len( context._F6_ms))
                context._PyrA_moy.append(sum( context._PyrA_ms)/len( context._PyrA_ms))
                context._PyrB_moy.append(sum( context._PyrB_ms)/len( context._PyrB_ms))
                context._PyrC_moy.append(sum( context._PyrC_ms)/len( context._PyrC_ms))
                
                context._vit_moy.append(sqrt(context._p1_moy[-1])*2/context._rho_air)                
                context._Tasp_moy.append((context._Tint1_moy[-1]+context._Tint2_moy[-1]+context._Tint3_moy[-1]+context._Tbe1_moy[-1]+context._Tbe2_moy[-1]+context._Tbe3_moy[-1])/(context._num_Tint+context._num_Tbe))
                context._Tbe_moy.append((context._Tbe1_moy[-1]+context._Tbe2_moy[-1]+context._Tbe3_moy[-1])/(context._num_Tbe))
                
                
                context._Pint_r_moy.append(1.29*context._vit_moy[-1]*pi*(0.315/2)**2*1006*(context._Ts_moy[-1]-context._Tasp_moy[-1]))                
                context._PBC_r_moy.append(1.29*context._vit_moy[-1]*pi*(0.315/2)**2*1006*(context._Ts_moy[-1]-context._Tbe_moy[-1]))              
                
                
                context._PBC_th.append(context._PBC_max)                 
                if context._Ts_moy[-1]>46:
                    context._pourcent=0
                    print('WARNING TEMPERATURE : hot batteries set to 0 W') 
                else:
                    context._pourcent=context._PBC_th[-1]/context._PBC_max
                context._BC.push_value(context._maq20_d, context._pourcent, current_time)
                
                print("Pint_r : "+str(context._Pint_r_moy[-1]))
                print("Pint_th : "+str(context._Pint_th[-1]))
                print("Tasp : " +str(context._Tasp_moy[-1])+" °C")           
                print("PBC_r : ", context._PBC_r_moy[-1])
                print("PBC_th : ", context._PBC_th[-1]) 
                print("Tbe : " +str(context._Tbe_moy[-1])+" °C") 
                print("vit : "+str(context._vit_moy[-1])+" m/s")
                print("p1 : " +str(context._p1_moy[-1])+" Pa")
                # print("Tint1 : " +str(context._Tint1_moy[-1])+" °C")
                # print("Tint2 : " +str(context._Tint2_moy[-1])+" °C")
                # print("Tint3 : " +str(context._Tint3_moy[-1])+" °C")
                # print("Tbe1 : " +str(context._Tbe1_moy[-1])+" °C")
                # print("Tbe2 : " +str(context._Tbe2_moy[-1])+" °C")
                # print("Tbe3 : " +str(context._Tbe3_moy[-1])+" °C")
                # print("Tbs1 : " +str(context._Tbs1_moy[-1])+" °C")
                # print("Tbs2 : " +str(context._Tbs2_moy[-1])+" °C")
                # print("Tbs3 : " +str(context._Tbs3_moy[-1])+" °C")
                print("Ts : " +str(context._Ts_moy[-1])+" °C")              
                            
                # print("F2 : " +str(context._F2_moy[-1])+" °C")
                # print("F3 : " +str(context._F3_moy[-1])+" °C")
                # print("F6 : " +str(context._F6_moy[-1])+" °C")
                print("PyrA : " +str(context._PyrA_moy[-1])+" °C")
                print("PyrB : " +str(context._PyrB_moy[-1])+" °C")
                print("PyrC : " +str(context._PyrC_moy[-1])+" °C")
                           
                fichier_acq.write(current_time+";"+
                                  str(context._Pint_th[-1])+";"+
                                  str(context._Pint_r_moy[-1])+";"+
                                  str(context._PBC_th[-1])+";"+
                                  str(context._PBC_r_moy[-1])+";"+
                                  str(context._vit_moy[-1])+";"+  # calcul sue la base de la moyenne de p1
                                  str(context._p1_moy[-1])+";"+
                                  str(context._Tint1_moy[-1])+";"+
                                  str(context._Tint2_moy[-1])+";"+
                                  str(context._Tint3_moy[-1])+";"+
                                  str(context._Tbe1_moy[-1])+";"+
                                  str(context._Tbe2_moy[-1])+";"+
                                  str(context._Tbe3_moy[-1])+";"+
                                  str(context._Tbs1_moy[-1])+";"+
                                  str(context._Tbs2_moy[-1])+";"+
                                  str(context._Tbs3_moy[-1])+";"+
                                  # str(sum(context._T4_moy)/len(context._T4_moy))+";"+
                                  str(context._Tasp_moy[-1])+";"+
                                  str(context._Ts_moy[-1])+";"+
                                  # str(sum(context._Tm_moy)/len(context._Tm_moy))+";"+
                                  str(context._PyrA_moy[-1])+";"+
                                  str(context._PyrB_moy[-1])+";"+
                                  str(context._PyrC_moy[-1])+";"+
                                  # str(sum(context._F1_moy)/len(context._F1_moy))+";"+
                                   str(context._F2_moy[-1])+";"+
                                   str(context._F3_moy[-1])+";"+
                                  # str(sum(context._F4_moy)/len(context._F4_moy))+";"+
                                  # str(sum(context._F5_moy)/len(context._F5_moy))+";"+
                                   str(context._F6_moy[-1])+";"+
                                  # str(sum(context._F7_moy)/len(context._F7_moy))+";"+
                                  # str(sum(context._F8_moy)/len(context._F8_moy))+
                                  "\n")
                       
                # compteur_ecriture+=1
                t2 = time()
                duree=t2-t1
                print('step duration : ',duree)
                print("waiting: ",60 - duree)
                while((Time.monotonic() - absolute_time) < 60):
                    sleep(0.1)
                    
            except:
                # compteur_ecriture+=1
                print("Error Communication! Retrying soon...")
                sleep(60)
                    
            
            i+=1    
            fichier_acq.close() 
            #fermer le fichier régulièrement permet de donner accès aux valeurs dans le fichier
            #et ainsi pouvoir faire du post-traitement en cours de route
                
                                                
class State_final(General_State):
    def __init__(self, is_simulation):
        super().__init__(is_simulation)
    

    def run(context):
        #Eteindre le ventilateur et la batterie chaude
        context._BC.push_value(context._maq20_d,0,"fin du protocole")
        sleep(180)
        context._Vent.push_value(context._maq20_d,0,"fin du protocole")

                
        print('#####################################################')
        print('#############   Fin du protocole   ################')
        print('#####################################################')








        
