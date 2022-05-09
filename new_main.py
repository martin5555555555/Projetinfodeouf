from re import M

from matplotlib.pyplot import connect
from nouveau_main_classes import *

#est on dans une simulation:
is_simulation = True
context = Context(is_simulation)
connect = State_connect(is_simulation)
init = State_init(context)
run = State_run(context)
final = State_final(context)
Machine = General_State(is_simulation= is_simulation)

Machine.run_from(connect)
Machine.run_from(init, context)
choice=input('Ecrire "start" pour demarer le code :')
if choice=='start':
    Machine.run_from(run, context)
else:
    Machine.run_from(init, context)


#Machine.run_from(State_final(context))