# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 16:54:45 2022

@author: wangz
"""

#from mapping import *
#from maq20 import MAQ20
from datetime import *
from time import *

from Instrument import Instrument

#######Sondes de temperature dans la salle#######

class Temp_PT100(Instrument):

    def __init__(self, name, channel, is_simulation):
        super().__init__(name, is_simulation)
        self.channel = channel
        #self.Tmin=Tmin
        #self.Tmax=Tmax
        self.module="S0153011-08"
        self.unit=" °C"
        
        
    def get_value_real(self, maq20,time):
        mod = maq20.find(self.module)
        
        if mod is None: # Check if module was not found
            raise ValueError("Module "+self.module+" for "+self.name+" not found")
            res=-1
        else:
            res=mod.read_channel_data(self.channel)
        
        self.log_value.append(res)
        self.log_time.append(time)
        return res
    
    def print_value(self):
        print(self.name+":"+str(self.log_value[-1])+self.unit)
        
 
#######Sondes de temperature sur la machine (on prend la moyenne)#######

class Temp_PT100_machine(Instrument):

    def __init__(self, name, channel1,channel2, is_simulation):
        super().__init__(name, is_simulation)
        self.channel1 = channel1
        self.channel2 = channel2
        #self.Tmin=Tmin
        #self.Tmax=Tmax
        self.module="S0153011-08"
        self.unit=" °C"
       
        
    def get_value_real(self, maq20,time):
        mod = maq20.find(self.module)
        
        if mod is None: # Check if module was not found
            raise ValueError("Module "+self.module+" for "+self.name+" not found")
            res=-1
        else:
            res=(mod.read_channel_data(self.channel1)+mod.read_channel_data(self.channel2))/2
        
        self.log_value.append(res)
        self.log_time.append(time)
        return res
    
    def print_value(self):
        print(self.name+":"+str(self.log_value[-1])+self.unit)
        
    
        
#######Fluxmeters#######

class Fluxmeter(Instrument):

    def __init__(self, name, channel, rate, is_simulation):
        super().__init__(name, is_simulation)
        self.channel = channel
        self.rate=rate
        self.module="S0134615-04"
        self.unit=" W/m^2"
        # self.unit=" V"
       
        
    def get_value_real(self, maq20, time):
        mod = maq20.find(self.module)
        
        if mod is None: # Check if module was not found
            raise ValueError("Module "+self.module+" for "+self.name+" not found")
            res=-1
        else:
            res=mod.read_channel_data(self.channel)
            res=res/self.rate
            
        self.log_value.append(res)
        self.log_time.append(time)
        return res

    def print_value(self):
        print(self.name+":"+str(self.log_value[-1])+self.unit)
        

#######controle pour ventilateur et batteries chaudes#######

class Controle(Instrument):

    def __init__(self, name, channel, Vmin, Vmax, is_simulation):
        super().__init__(name, is_simulation)
        self.channel = channel
        self.Vmin=Vmin
        self.Vmax=Vmax
        self.module="S0153470-04"
        self.unit=" V"
       
    
    def push_value_real(self, maq20, pourcent, time):
        mod = maq20.find(self.module)
        
        if(pourcent<0):
            pourcent=0
        if pourcent>1:
            pourcent=1
        
        if mod is None: # Check if module was not found
            raise ValueError("Module "+self.module+" for "+self.name+" not found")
            res=-1
        else:
            print("Verif Controle : 111")
            res=pourcent*(self.Vmax-self.Vmin)+self.Vmin
            mod.write_channel_data(channel = self.channel, data = res)
            
            
        self.log_value.append(res)
        self.log_time.append(time)
        return res
        
    def print_value(self):
        print(self.name+":"+str(self.log_value[-1])+self.unit)
        
  

#######Capteurs de pression#######

class Cap_pression(Instrument):

    def __init__(self, name, channel, Vmin, Vmax, Pmin, Pmax, is_simulation):
        super().__init__(name, is_simulation)
        self.channel = channel
        self.Vmin=Vmin
        self.Vmax=Vmax
        self.Pmin=Pmin
        self.Pmax=Pmax
        self.module="S0143330-08"
        self.unit=" Pa"
        
        
    def get_value_real(self, maq20, time):
        mod = maq20.find(self.module)
        #print('################## TEST DEBUGGGG ##################')
        #print ('pressionName : ',self.name)
        #print ('pressionChannel : ',self.channel)
        #print ('pressionMod : ',mod)
        #print ('pressionVmin : ',self.Vmin)
        #print ('pressionVmax : ',self.Vmax)
        if mod is None: # Check if module was not found
            raise ValueError("Module "+self.module+" for "+self.name+" not found")
            res=-1
        else:
            res=mod.read_channel_data(self.channel)
            #print("pressionRes : ",res)
            #print('################## FIN TEST DEBUGGGG ##################')
            res=(res-self.Vmin)*(self.Pmax-self.Pmin)/(self.Vmax-self.Vmin)+self.Pmin
            
        self.log_value.append(res)
        self.log_time.append(time)
        return res
   
    def print_value(self):
        print(self.name+":"+str(self.log_value[-1])+self.unit)
            
  
#######Pyranometers#######
     
class Pyrano(Instrument):

    def __init__(self, name, channel, is_simulation):
        super().__init__(name, is_simulation)
        self.channel = channel
        self.module="S0155245-15"
        self.unit=" mA"
      
        
    def get_value_real(self, maq20, time):
        mod = maq20.find(self.module)
        
        if mod is None: # Check if module was not found
            raise ValueError("Module "+self.module+" for "+self.name+" not found")
            res=-1
        else:
            res=mod.read_channel_data(self.channel)*1000
            
        self.log_value.append(res)
        self.log_time.append(time)
        return res
    
    def print_value(self):
        print(self.name+":"+str(self.log_value[-1])+self.unit)
    
  


#######other useful funcitons#######

def cal_delta_P(rho, vit, section, cp, T_asp, T_melange):
    dP=rho*vit*section*cp*(T_asp-T_melange)
    return dP

def cal_Pbat_r(rho, vit, section, cp, T_asp, T_souf): 
    #calculer Pbatiment,reelle
    Pbat_r=rho*vit*section*cp*(T_souf-T_asp)
    return Pbat_r

def cal_PBC_r(rho, vit, section, cp, T_melange, T_souf):
    PBC_r=rho*vit*section*cp*(T_souf-T_melange)
    return PBC_r

def cal_ARD(reelle, theorie):
    #calculate the absolute relative deviation
    ARD=abs((reelle-theorie)/theorie)
    return ARD
