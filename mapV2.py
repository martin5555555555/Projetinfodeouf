# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 16:37:13 2022

@author: wangz
"""

#Mapping for all sensors

# import numpy as np
from ProtoV2 import *

#######Temperatures(PT100)#######

#Inside the room

#number of T int
num_Tint=2

#T1
#T1=Temp_PT100(name = "T1", channel = 1, Tmin = 0, Tmax = 100)
T1=Temp_PT100(name = "T1", channel = 0)

#T2
#T2=Temp_PT100(name = "T2", channel = 2, Tmin = 0, Tmax = 100)
T2=Temp_PT100(name = "T2", channel = 1)

#T3
#T2=Temp_PT100(name = "T2", channel = 2, Tmin = 0, Tmax = 100)
T3=Temp_PT100(name = "T3(sortie de la batterie chaude)", channel = 3)

#...

#On the machine

#T_soufflage
Ts=Temp_PT100(name = "T_soufflage", channel = 2)

#T_melange
Tm=Temp_PT100(name = "T_melange", channel = 4)

#######Fluxmeter#######

#F1
F1=Fluxmeter(name = "Fluxmeter_9", channel = 0, rate = 126/1000000)

#F2
F2=Fluxmeter(name = "Fluxmeter_4", channel = 1, rate = 132/1000000)

#F3
F3=Fluxmeter(name = "Fluxmeter_2", channel = 2, rate = 269/1000000)

#F4
F4=Fluxmeter(name = "Fluxmeter_1", channel = 3, rate = 119/1000000)

#F5
F5=Fluxmeter(name = "Fluxmeter_6", channel = 4, rate = 136/1000000)

#F6
F6=Fluxmeter(name = "Fluxmeter_3", channel = 5, rate = 284/1000000)

#F7
F7=Fluxmeter(name = "Fluxmeter_5", channel = 6, rate = 132/1000000)

#F8
F8=Fluxmeter(name = "Fluxmeter_3small", channel = 7, rate = 130/1000000)

#######Capteur de pression#######

#P1
P1=Cap_pression(name = "Pression_2", channel = 0, Vmin = 0, Vmax = 10, Pmin = 0, Pmax = 100)

#P2
P2=Cap_pression(name = "Pression_1", channel = 1, Vmin = 0, Vmax = 10, Pmin = 0, Pmax = 500)

#######Controle#######

#Ventilateur
Ven=Controle(name = "Controle_Ventilateur", channel = 0, Vmin = 0, Vmax = 10)

#Batterie Chaude
Bat=Controle(name = "Control_BC", channel = 1, Vmin = 0, Vmax = 10)

#######Pyranometer#######

#Pyrano
PyrA=Pyrano(name = "PyranoA", channel = 0)

#PyranoB
PyrB=Pyrano(name = "PyranoB", channel = 1)

#Contrôle de Pbat_th
#je prends la consigne de Morgane (pas de temps de temps de 1minute, durée = 4 jours)
from consigneBureauFred import *
# from consigne_test import *

sollicitation_P= consigne_PBC #consigne de contrôle de P_réelle (format à voir)

def print_all():
    
    T1.print_value()
    T2.print_value()
    T3.print_value()
    Tm.print_value()
    Ts.print_value()
    
    P1.print_value()
    P2.print_value()
    
    Ven.print_value()
    Bat.print_value()
    
    F1.print_value()
    F2.print_value()
    F3.print_value()
    F4.print_value()
    F5.print_value()
    F6.print_value()
    F7.print_value()
    F8.print_value()
    
    PyrA.print_value()
    PyrB.print_value()