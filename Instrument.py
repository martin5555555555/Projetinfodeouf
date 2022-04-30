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
            return self.get_value_real(maq20, pourcent, time)

    def get_value(self, maq20,time):
        
        if self.is_simulation:
            res = generate_value_simulation()
           
        else:
            res = self.get_value_real(maq20, time)
        self.log_value.append(res)
        self.log_time.append(time)
        return res
    
    def clear(self):
        self.log_value=[]
        self.log_time=[]
