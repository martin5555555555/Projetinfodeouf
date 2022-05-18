from mapV2 import *
from ProtoV2 import *
from maq20 import MAQ20

import time as Time
from time import time
from datetime import datetime
from math import *
#je prends la consigne de Morgane (pas de temps de temps de 1minute, durée = 4 jours)
from consigneBureauFred import *
from ProtoV2 import *


class Context:
    def __init__(self, is_simulation):
        self._name = "Name + date etc?..."
        self._is_simulation = is_simulation
        
        self._T1=Temp_PT100(name = "T1", channel = 0, is_simulation = self._is_simulation,module="S0153011-08")
        #T2
        #T2=Temp_PT100(name = "T2", channel = 2, Tmin = 0, Tmax = 100)
        self._T2=Temp_PT100(name = "T2", channel = 1, is_simulation = self._is_simulation,module="S0153011-08")
        self._T3=Temp_PT100(name = "T3(sortie de la batterie chaude)", channel = 3, is_simulation = self._is_simulation,module="S0153011-08")
        self._T4=Temp_PT100(name = "T4", channel = 0, is_simulation = self._is_simulation,module="S0153011-07")
        
        #On the machine

        #T_soufflage
        self._Ts=Temp_PT100(name = "T_soufflage", channel = 2, is_simulation = self._is_simulation,module="S0153011-08")
        #T_melange
        self._Tm=Temp_PT100(name = "T_melange", channel = 4, is_simulation = self._is_simulation,module="S0153011-08")

        #######Fluxmeter#######

        #F1
        self._F1=Fluxmeter(name = "Fluxmeter_9", channel = 0, rate = 126/1000000, is_simulation = self._is_simulation)

        #F2
        self._F2=Fluxmeter(name = "Fluxmeter_4", channel = 1, rate = 132/1000000, is_simulation = self._is_simulation)

        #F3
        self._F3=Fluxmeter(name = "Fluxmeter_2", channel = 2, rate = 269/1000000, is_simulation = self._is_simulation)

        #F4
        self._F4=Fluxmeter(name = "Fluxmeter_1", channel = 3, rate = 119/1000000, is_simulation = self._is_simulation)

        #F5
        self._F5=Fluxmeter(name = "Fluxmeter_6", channel = 4, rate = 136/1000000, is_simulation = self._is_simulation)

        #F6
        self._F6=Fluxmeter(name = "Fluxmeter_3", channel = 5, rate = 284/1000000, is_simulation = self._is_simulation)

        #F7
        self._F7=Fluxmeter(name = "Fluxmeter_5", channel = 6, rate = 132/1000000, is_simulation = self._is_simulation)

        #F8
        self._F8=Fluxmeter(name = "Fluxmeter_3small", channel = 7, rate = 130/1000000, is_simulation = self._is_simulation)

        #######Capteur de pression#######

        #P1
        self._P1=Cap_pression(name = "Pression_2", channel = 0, Vmin = 0, Vmax = 10, Pmin = 0, Pmax = 100, is_simulation = self._is_simulation)

        #P2
        self._P2=Cap_pression(name = "Pression_1", channel = 1, Vmin = 0, Vmax = 10, Pmin = 0, Pmax = 500, is_simulation = self._is_simulation)

        #######Controle#######

        #Ventilateur
        self._Ven=Controle(name = "Controle_Ventilateur", channel = 0, Vmin = 0, Vmax = 10, is_simulation = self._is_simulation)

        #Batterie Chaude
        self._Bat=Controle(name = "Control_BC", channel = 1, Vmin = 0, Vmax = 10, is_simulation = self._is_simulation)

        #######Pyranometer#######

        #Pyrano
        self._PyrA=Pyrano(name = "PyranoA", channel = 0, is_simulation = self._is_simulation)

        #PyranoB
        self._PyrB=Pyrano(name = "PyranoB", channel = 1, is_simulation = self._is_simulation)

        #Contrôle de Pbat_th
        # from consigne_test import *

        self._sollicitation_P= consigne_PBC#[5 for i in range (60*24*5+5)]#consigne_PBC #consigne de contrôle de P_réelle (format à voir)

        #...
        
        #mettre toutes les valeusr de mapV2 ici

        #ToDO: entrer tous les Instruments pressions initialement à la valeur none, et aussi les consignes et les puissances
        self._Ini_time = str(datetime.now()).split(",")[0].replace("-", "_")
        self._Ini_time = self._Ini_time.replace(":", "_")
        self._T_asp = []
        self._Pbat_th = []
        self._Pbat_r = []
        self._vit = []
        self._PBC_th = []
        self._PBC_r = []
        self._diameter=0.315 #TODO indiquer la bonne valeur
        self._section = 1*pi*(self._diameter/2)**2 #0.8165
        self._cp_air = 1005 #TODO indiquer la bonne valeur
        self._rho_air = 1.29  #TODO indiquer la bonne valeur 
        self._PBC_max=6000
        self._maq20_d=None
        self._num_Tint = 3
        self._pourcent = None
        self._pourcent_vent = None

    def cal_delta_P(self):
        dP=self._rho_air* self._vit[-1]*self._section*self._cp_air*(self._T_asp[-1]-self._Tm.log_value[-1])
        return dP

    def cal_Pbat_r(self): 
        #calculer Pbatiment,reelle
        Pbat_r=self._rho_air*self._vit[-1]*self._section*self._cp_air*(self._Ts.log_value[-1]-self._T_asp[-1])
        return Pbat_r

    def cal_PBC_r(self):
        PBC_r=self._rho_air*self._vit[-1]*self._section*self._cp_air*(self._Ts.log_value[-1]-self._Tm.log_value[-1])
        return PBC_r

    def cal_ARD(self, reelle, theorie):
        #calculate the absolute relative deviation
        if(theorie==0 or (reelle-theorie)==0):
            print("error cal_ARD : reelle "+str(reelle)+", theorie "+str(theorie))
            return 0
        ARD=abs((reelle-theorie)/theorie)
        return ARD
    def print_all(self):
        self._T1.print_value()
        self._T2.print_value()
        self._T3.print_value()
        self._T4.print_value()
        self._Tm.print_value()
        self._Ts.print_value()
        
        self._P1.print_value()
        self._P2.print_value()
        
        self._Ven.print_value()
        self._Bat.print_value()
        
        #self._F1.print_value()
        #self._F2.print_value()
        self._F3.print_value()
        #self._F4.print_value()
        self._F5.print_value()
        self._F6.print_value()
        #self._F7.print_value()
        #self._F8.print_value()
        
        self._PyrA.print_value()
        self._PyrB.print_value()




    

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
        input_PBC_th = float(input('Puissance Batterie Chaude theorique (PBC_th) injectée (W)'))
        context._PBC_th.append(input_PBC_th)
        context._pourcent=context._PBC_th[-1]/context._PBC_max
        print(context._pourcent)
        context._Bat.push_value(context._maq20_d, context._pourcent, current_time)
        
        #Puissance ventilateur
        context._pourcent_vent=float(input('Puissance ventilateur (%)'))/100
        context._Ven.push_value(context._maq20_d, context._pourcent_vent,current_time)

        counter2=0
        print_it =  3
        for i in range (print_it):
            counter2 += 1
            context._current_time=(current_time+"."+str(counter2))
                
            wait= 0
            print('Please wait for '+str(wait)+' second(s)')
            print(P2.log_value)
            sleep(wait)
                
             
            context._vit.append(sqrt(context._P2.get_value(context._maq20_d,current_time)*2/context._rho_air))
            print("vit : "+str(context._vit[-1])+" m/s")
            context._P1.get_value(context._maq20_d,current_time)
            context._P1.print_value()
                    
            context._T_asp.append((context._T1.get_value(context._maq20_d,current_time)+context._T2.get_value(context._maq20_d,current_time))/context._num_Tint)
            context._T1.print_value()
            context._T2.print_value()
            context._T3.get_value(context._maq20_d,current_time)
            context._T3.print_value()
            context._T4.get_value(context._maq20_d,current_time)
            context._T4.print_value()
            print("T_asp : "+str(context._T_asp[-1])+" °C")
                
            context._Tm.get_value(context._maq20_d,current_time)
            context._Ts.get_value(context._maq20_d,current_time)
            context._Tm.print_value()
            context._Ts.print_value()
                    
            context._Pbat_th.append(context._PBC_th[-1]- context.cal_delta_P() )
            print("Pbat_th : "+str(context._Pbat_th[-1])+" W")
                    
            context._Pbat_r.append(context.cal_Pbat_r())
            print("Pbat_r : "+str(context._Pbat_r[-1])+" W")
                    
            e = cal_ARD(context._Pbat_r[-1],context._Pbat_th[-1])
            print("Différence entre Pbat_r et Pbat_th est : "+str(e*100)+" %")

            
   
        
class State_run(General_State):
    def __init__(self, is_simulation):
        super().__init__(is_simulation)

    def run(self, context):
        name_file='Initialiasation_Values_'+context._Ini_time+'.csv'
        fichier_acq=open(name_file, 'w')
        fichier_acq.write("date_time;P1 - [Pa];P2 - [Pa];Pbat - [W];T1 [°C];T2 [°C];T3 [°C];T_asp [°C];Tm [°C];Ts [°C];vitesse_air - [m/s];Pbat_r - [W]; Pbat_th - [W]\n")
        fichier_acq.write(str(context._T1.log_time)+";"+str(context._P1.log_value)+";"+str(context._P2.log_value)+";"+str(context._T1.log_value)+";"+str(context._T2.log_value)+";"+str(context._T3.log_value)+";"+str(context._T_asp)+";"+str(Tm.log_value)+";"+str(context._Ts.log_value)+";"+str(context._vit)+";"+str(context._Pbat_r)+";"+str(context._Pbat_th)+";\n")
        
        
        count = 0
        sleep(1)
        count=count+1
        ###############################################################################
        ######################################################################
        ##############################################################################
        print('#############   Paramètres initiaux   ################')
        print(P2.log_value)

        print('Pourcentage choisie des ventilateurs :', context._pourcent*100 , '%')
        print('Vitesse de l\'air :', context._vit[-1], 'm/s')
        print('Sur-pression obtenue dans le bâtiment :', context._P2.log_value[-1], 'Pa')
        print('Puissance réelle désirée :', context._Pbat_th[-1], 'W')
        print('Puissance des batteries chaudes correspondant :', context._PBC_th, 'W')
        print('Puissance réelle injectée :', context._Pbat_r[-1], 'W')

        print('#####################################################')
        print('#############   Début du protocole   ################')
        print('#####################################################')
        current_time=str(datetime.now())

        context._vit.append(sqrt(context._P2.get_value(context._maq20_d,current_time)*2/context._rho_air))
        context._P1.get_value(context._maq20_d,current_time)

        context._T_asp.append((context._T1.get_value(context._maq20_d,current_time)+context._T2.get_value(context._maq20_d,current_time))/context._num_Tint)
        context._T3.get_value(context._maq20_d,current_time)
        context._T4.get_value(context._maq20_d,current_time)
        context._Tm.get_value(context._maq20_d,current_time)
        context._Ts.get_value(context._maq20_d,current_time)
        context._F1.get_value(context._maq20_d,current_time)
        context._F2.get_value(context._maq20_d,current_time)
        context._F3.get_value(context._maq20_d,current_time)#
        context._F4.get_value(context._maq20_d,current_time)
        context._F5.get_value(context._maq20_d,current_time)
        context._F6.get_value(context._maq20_d,current_time)#
        context._F7.get_value(context._maq20_d,current_time)
        context._F8.get_value(context._maq20_d,current_time)
        context._PyrA.get_value(context._maq20_d,current_time)
        context._PyrB.get_value(context._maq20_d,current_time)

        context.print_all()

        #TODO premiere valeur : 0 pour débuter au début... ou alors une autre valeur
        i=425

        context._Pbat_th.append(context._sollicitation_P[i]*2/3)
        print("Pbat_th : "+str(context._Pbat_th[-1])+" W")

        context._PBC_th.append(context._Pbat_th[-1]+context.cal_delta_P())
        pourcent=context._PBC_th[-1]/context._PBC_max
        context._Bat.push_value(context._maq20_d, pourcent, current_time)
        print("PBC_th : "+str(context._PBC_th[-1])+" W")
                
        context._Pbat_r.append(context.cal_Pbat_r())
        print("Pbat_r : "+str(context._Pbat_r[-1])+" W")

        context._PBC_r.append(context.cal_PBC_r())
        print("PBC_r : "+str(context._PBC_r[-1])+" W")

        e_bat=context.cal_ARD(context._Pbat_r[-1],context._Pbat_th[-1])
        print("Différence entre Pbat_r et Pbat_th est : "+str(e_bat*100)+" %")
                
        e_BC=context.cal_ARD(context._PBC_r[-1],context._PBC_th[-1])
        print("Différence entre PBC_r et PBC_th est : "+str(e_BC*100)+" %")

        #fichier d'acquisition

        nametime=str(datetime.now()).split(".")[0].replace("-", "_")
        nametime=nametime.replace(":", "_")
        name_file='ProtoZW_test2'+nametime+'.csv'
        fichier_acq=open(name_file, 'w') #création d'un nouveau fichier seulement si celui-ci n'existe pas : sinon ERROR
        #TODO adapter la premiere ligne a chaque experience
        fichier_acq.write("date;Pconsigne(Pbat_th) - [W];Pbat_r - [W];PBC_th - [W];PBC_r - [W];vitesse_air - [m/s];sur-pression - [Pa];T1;T2;T3;T4;T_asp;Ts;Tm;pyranoA;pyranoB;flux 9;flux 2;flux 2;flux 3;flux 4;flux 5;flux 6;flux 7\n")
        fichier_acq.write(current_time+";"+str(context._Pbat_th[-1])+";"+str(context._Pbat_r[-1])+";"+str(context._PBC_th[-1])+";"+str(context._PBC_r[-1])+";"+str(context._vit[-1])+";"+str(context._P1.log_value[-1])+";"+str(context._T1.log_value[-1])+";"+str(context._T2.log_value[-1])+";"+str(context._T3.log_value[-1])+";"+str(context._T_asp[-1])+";"+str(context._Ts.log_value[-1])+";"+str(context._Tm.log_value[-1])+";"+str(context._PyrA.log_value[-1])+";"+str(context._PyrB.log_value[-1])+";"+str(context._F1.log_value[-1])+";"+str(context._F2.log_value[-1])+";"+str(context._F3.log_value[-1])+";"+str(context._F4.log_value[-1])+";"+str(context._F5.log_value[-1])+";"+str(context._F6.log_value[-1])+";"+str(context._F7.log_value[-1])+";"+str(context._F8.log_value[-1])+"\n")
        fichier_acq.close()

        l=len(context._sollicitation_P)

        # temps_pression=0
        while i<(l):
            context._P1_moy = []
            context._P2_moy = []
            context._Tm_moy = []
            context._Ts_moy = []
            context._T1_moy = []
            context._T2_moy = []
            context._T3_moy = []
            context._T4_moy = []
            context._F1_moy = []
            context._F2_moy = []
            context._F3_moy = []
            context._F4_moy = []
            context._F5_moy = []
            context._F6_moy = []
            context._F7_moy = []
            context._F8_moy = []
            context._PyrA_moy = []
            context._PyrB_moy = []
            absolute_time = Time.monotonic()
            compteur_ecriture=0 #pour voir tous les combien de ligne on ferme le fichier et on le rouvre
            fichier_acq=open(name_file, 'a')   #ouverture en mode "append"


            t1 = time()
            try:
                current_time=str(datetime.now())
                
                
                context._Pbat_th.append(context._sollicitation_P[i]*2/3) #TODO coeff de modif consigne
                
                ##sécurité avant la pause
                if context._pourcent_vent==0 or context._vit[-1]<0.05 :   #sécurité vis à vis de la ventilation : il faut qu'il y ait une circulation d'air pour allumer les BC
        
                    fichier_acq.write(current_time+";ERROR - SAFETY : P_BC = 0"+"\n")
                    print('ERROR VENTILATION')
                    pourcent=0
                    context._Bat.push_value(context._maq20_d,pourcent,current_time) #mise à 0 de PBC
                    
                
                #calculer PBC
                print(' ')
                print('Target step '+str(i)+'/'+str(l)+' : '+str(context._Pbat_th[-1])+' W')
                print("Consigne : "+str(context._sollicitation_P[i]*2/3)+' W')
                context._PBC_r.append(context.cal_PBC_r())
                print('Puissance batterie chaude réelle: '+str(context._PBC_r[-1])+' W')
                ##sécurité après la pause (à voir si vraiment utile - temps d'exécution entre 2 pauses assez court)
                print('Air speed : '+str(context._vit[-1]))
                if context._pourcent_vent==0 or context._vit[-1]<0.05 :   #sécurité vis à vis de la ventilation : il faut qu'il y ait une circulation d'air pour allumer les BC
        
                    fichier_acq.write("ERROR - SAFETY : P_BC = 0"+"\n")
                    print('ERROR VENTILATION')
                    pourcent=0
                    context._Bat.push_value(context._maq20_d,pourcent,current_time) #mise à 0 de PBC
                    #Il faudrait voir pour réimposer une vitesse d'air... sinon cela ne repartira pas !! Mais quelle vitesse ?
                
                
                sleep(5)
                #aqcuérir toutes les grandeurs nécessaires
                #TODO ajouter toutes les températures et tous les flux
                
        
                
                print("acquisition + averaging")
                while ((Time.monotonic() - absolute_time) < 55) : #TODO needs to be 60
                    current_time=str(datetime.now())
                    context._P1_moy.append(context._P1.get_value(context._maq20_d,current_time))
                    context._P2_moy.append(context._P2.get_value(context._maq20_d,current_time))
                    context._Tm_moy.append(context._Tm.get_value(context._maq20_d,current_time))
                    context._Ts_moy.append(context._Ts.get_value(context._maq20_d,current_time))
                    context._T1_moy.append(context._T1.get_value(context._maq20_d,current_time))
                    context._T2_moy.append(context._T2.get_value(context._maq20_d,current_time))
                    context._T3_moy.append(context._T3.get_value(context._maq20_d,current_time))
                    context._T4_moy.append(context._T4.get_value(context._maq20_d,current_time))
            
                    context._F1_moy.append(context._F1.get_value(context._maq20_d,current_time))
                    context._F2_moy.append(context._F2.get_value(context._maq20_d,current_time))
                    context._F3_moy.append(context._F3.get_value(context._maq20_d,current_time))#
                    context._F4_moy.append(context._F4.get_value(context._maq20_d,current_time))
                    context._F5_moy.append(context._F5.get_value(context._maq20_d,current_time))
                    context._F6_moy.append(context._F6.get_value(context._maq20_d,current_time))#
                    context._F7_moy.append(context._F7.get_value(context._maq20_d,current_time))
                    context._F8_moy.append(context._F8.get_value(context._maq20_d,current_time))
        
                    context._PyrA_moy.append(context._PyrA.get_value(context._maq20_d,current_time))
                    context._PyrB_moy.append(context._PyrB.get_value(context._maq20_d,current_time))
                    sleep(0.5)


                context._vit.append(sqrt((sum( context._P2_moy)/len( context._P2_moy))*2/ context._rho_air))
                context._T_asp.append(((sum( context._T1_moy)/len( context._T1_moy))+(sum( context._T2_moy)/len( context._T2_moy))+(sum( context._T4_moy)/len( context._T4_moy)))/ context._num_Tint) 
                context.print_all()
                
                # context._Pbat_th.append(context._sollicitation_P[i]*2/3) #TODO coeff de modif consigne
        
                context._PBC_th.append(context._Pbat_th[-1]+context.cal_delta_P())
                
                if context._Ts.log_value[-1]>50:
                    context._pourcent=0
                    print('WARNING TEMPERATURE : hot batteries set to 0 W') 
                else:
                    context._pourcent=context._PBC_th[-1]/context._PBC_max
                print("Percent applied to Batteries: "+str(context._pourcent)+' %')
                context._Bat.push_value(context._maq20_d, context._pourcent, current_time)
                
                context._Pbat_r.append(context.cal_Pbat_r())
        
                context._PBC_r.append(context.cal_PBC_r())
                e_bat=context.cal_ARD(context._Pbat_r[-1],context._Pbat_th[-1])
                print("Pbat_r : ", context._Pbat_r[-1])
                print("Pbat_th : ", context._Pbat_th[-1])
                print("Différence entre Pbat_r et Pbat_th est : "+str(e_bat*100)+" %")
                
                e_BC=context.cal_ARD(context._PBC_r[-1],context._PBC_th[-1])
                print("PBC_r : ", context._PBC_r[-1])
                print("PBC_th : ", context._PBC_th[-1])
                print("Différence entre PBC_r et PBC_th est : "+str(e_BC*100)+" %")
        

                #enregistrer tout ce que l'on veut dans le fichier csv
                #TODO adapter cette ligne a chaque experimentation
                fichier_acq.write(current_time+";"+str(context._Pbat_th[-1])+";"+str(context._Pbat_r[-1])+";"+str(context._PBC_th[-1])+";"+str(context._PBC_r[-1])+";"+str(context._vit[-1])+";"+str(sum(context._P1_moy)/len(context._P1_moy))+";"+str(sum(context._T1_moy)/len(context._T1_moy))+";"+str(sum(context._T2_moy)/len(context._T2_moy))+";"+str(sum(context._T3_moy)/len(context._T3_moy))+";"+str(sum(context._T4_moy)/len(context._T4_moy))+";"+str(context._T_asp[-1])+";"+str(sum(context._Ts_moy)/len(context._Ts_moy))+";"+str(sum(context._Tm_moy)/len(context._Tm_moy))+";"+str(sum(context._PyrA_moy)/len(context._PyrA_moy))+";"+str(sum(context._PyrB_moy)/len(context._PyrB_moy))+";"+str(sum(context._F1_moy)/len(context._F1_moy))+";"+str(sum(context._F2_moy)/len(context._F2_moy))+";"+str(sum(context._F3_moy)/len(context._F3_moy))+";"+str(sum(context._F4_moy)/len(context._F4_moy))+";"+str(sum(context._F5_moy)/len(context._F5_moy))+";"+str(sum(context._F6_moy)/len(context._F6_moy))+";"+str(sum(context._F7_moy)/len(context._F7_moy))+";"+str(sum(context._F8_moy)/len(context._F8_moy))+"\n")
                
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
        context._Bat.push_value(context._maq20_d,0,"fin du protocole")
        sleep(180)
        context._Ven.push_value(context._maq20_d,0,"fin du protocole")

                
        print('#####################################################')
        print('#############   Fin du protocole   ################')
        print('#####################################################')








        
