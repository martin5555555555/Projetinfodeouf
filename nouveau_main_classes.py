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
            Bat.push_value(maq20_d, pourcent, current_time)
            
            #Puissance ventilateur
            pourcent_vent=float(input('Puissance ventilateur (%)'))/100
            Ven.push_value(maq20_d, pourcent_vent,current_time)

            
