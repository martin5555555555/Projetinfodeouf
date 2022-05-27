def generate_value_simulation():
    return 5

class Instrument:
    def __init__(self, name, is_simulation = False):
        self.name = name
        self.log_value=[]
        self.log_time=[]
        self.is_simulation = is_simulation



    def push_value(self, maq20,pourcent, time):
        
        if self.is_simulation:
            self.log_value.append(pourcent)
            self.log_time.append(time)
        else:
            
            res= self.push_value_real(maq20, pourcent, time)
            # print("voltageOutput_instrument :"+str(res))
            
        if(len(self.log_value)>100):
            for i in range(10):
                self.log_value.pop()
        
        if(len(self.log_time)>100):
            for i in range(10):
                self.log_time.pop()

    def get_value(self, maq20,time):
        
        if self.is_simulation:
            res = generate_value_simulation()
           
        else:
            res = self.get_value_real(maq20, time)
        self.log_value.append(res)
        self.log_time.append(time)
        if(len(self.log_value)>100):
            for i in range(10):
                self.log_value.pop()
        
        if(len(self.log_time)>100):
            for i in range(10):
                self.log_time.pop()
        return res
    
    def get_value_real(self, maq20,time):
        return -1
    
    def push_value_real(self, maq20, pourcent, time):
        return -1
    
    def clear(self):
        self.log_value=[]
        self.log_time=[]
