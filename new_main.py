from re import M

from matplotlib.pyplot import connect
from michael import *

#est on dans une simulation:
is_simulation = False
context_i = Context(is_simulation)
connect = State_connect(is_simulation)
init = State_init(context_i)
run = State_run(context_i)
final = State_final(context_i)
Machine = General_State(is_simulation= is_simulation)
print("step0")
Machine.run_from(connect, context_i)
print("step1")
print(context_i._maq20_d)
Machine.run_from(init, context_i)
print("step2")
choice=input('Ecrire "s" pour demarer le code :')
if choice=='s':
    Machine.run_from(run, context_i)
else:
    Machine.run_from(init, context_i)
Machine.run_from(final,context_i)