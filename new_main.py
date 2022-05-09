from re import M
from nouveau_main_classes import *
context = Context()
init = State_init(context)
run = State_run(context)
final = State_final(context)
Machine = General_State(is_simulation= True)

Machine.run_from(init, context)
Machine.run_from(run, context)
Machine.run_from(State_final(context))