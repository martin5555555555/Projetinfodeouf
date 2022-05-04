class Context:
    def __init__(self):
        self._name = "Name + date etc?..."
        self._is_simulation = True
        
        self._T1=Temp_PT100(name = "T1", channel = 0, is_simulation= simulation)
        #mettre toutes les valeusr de mapV2 ici

        #ToDO: entrer tous les Instruments pressions initialement à la valeur none, et aussi les consignes et les puissances
        self._Ini_time = str(datetime.now()).split(",")[0].replace("-", "_")
        self._Ini_time = Ini_time.replace(":", "_")
        self._T_asp = []
        self._Pbat_th = []
        self._Pbat_r = []
        self._vit = []
        self._PBC_th = []
        self._PBC_r = []
        self._diameter=0.315 #TODO indiquer la bonne valeur
        self._section = 1*pi*(diameter/2)**2 #0.8165
        self._cp_air = 1005 #TODO indiquer la bonne valeur
        self._rho_air = 1.29  #TODO indiquer la bonne valeur 
        self._PBC_max=6000

    

class General_State(Context):
    def __init__(self, is_simulation):
        self._is_simulation = is_simulation

    def run_from(self, state, context):
        while state is not None:
            state = state.run(context)

class State_init(General_state):
    def __init__(self, is_simulation):
        super().__init__(is_simulation)

    def run(context):

        nbofattempt=0

        #connection
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

        print("connection success")

        while True:

            current_time=('init_'+str(count))
    
            #Réglage puissance réelle désirée
            PBC_th = float(input(input('Puissance Batterie Chaude theorique (PBC_th) injectée (W)')))
            context._PBC_th.append(PBC_th)
            pourcent=PBC_th[-1]/PBC_max
            print(pourcent)
            context._Bat.push_value(maq20_d, pourcent, current_time)
            
            #Puissance ventilateur
            pourcent_vent=float(input('Puissance ventilateur (%)'))/100
            context._Bat.Ven.push_value(maq20_d, pourcent_vent,current_time)
            counter2=0
    
            print_it =  3
            for i in range (print_it):
                counter2 += 1
                context._current_time=(current_time+"."+str(counter2))
                
                wait= 5 
                print('Please wait for '+str(wait)+' second(s)')
                
                sleep(wait)
                
                
                context._vit.append(sqrt(P2.get_value(maq20_d,current_time)*2/rho_air))
                print("vit : "+str(vit[-1])+" m/s")
                context._P1.get_value(maq20_d,current_time)
        context._P1.print_value()
        
        context._T_asp.append((context._T1.get_value(maq20_d,current_time)+context._T2.get_value(maq20_d,current_time))/context._num_Tint)
        context._T1.print_value()
        context._T2.print_value()
        context._T3.get_value(maq20_d,current_time)
        context._T3.print_value()
        print("T_asp : "+str(Context._T_asp[-1])+" °C")
        
        context._Tm.get_value(maq20_d,current_time)
        context._Ts.get_value(maq20_d,current_time)
        context._Tm.print_value()
        context._Ts.print_value()
        
        context._Pbat_th.append(PBC_th[-1]-cal_delta_P(context.rho_air, context._vit[-1], context._section, context._cp_air, context._T_asp[-1], context._Tm.log_value[-1]))
        print("Pbat_th : "+str(context._Pbat_th[-1])+" W")
        
        context._Pbat_r.append(context._cal_Pbat_r(context.rho_air, context._vit[-1], context._section, context._cp_air, context._T_asp[-1], context._Ts.log_value[-1]))
        print("Pbat_r : "+str(Pbat_r[-1])+" W")
        
        e = cal_ARD(context._Pbat_r[-1],context._Pbat_th[-1])
        print("Différence entre Pbat_r et Pbat_th est : "+str(e*100)+" %")

        choice = input('Ecrire "start" pour demarer le code :')

        if choice == 'start':
                
                name_file = 'Initialiasation_Values_'+Ini_time+'.csv'
                fichier_acq = open(name_file, 'w')
                fichier_acq.write("date_time;P1 - [Pa];P2 - [Pa];Pbat - [W];T1 [°C];T2 [°C];T3 [°C];T_asp [°C];Tm [°C];Ts [°C];vitesse_air - [m/s];Pbat_r - [W]; Pbat_th - [W]\n")
                fichier_acq.write(str(T1.log_time)+";"+str(P1.log_value)+";"+str(P2.log_value)+";"+str(T1.log_value)+";"+str(T2.log_value)+";"+str(T3.log_value)+";"+str(T_asp)+";"+str(Tm.log_value)+";"+str(Ts.log_value)+";"+str(vit)+";"+str(Pbat_r)+";"+str(Pbat_th)+";\n")
                
                break
            
        sleep(1)
        count=count+1
   
        

           
           


            
