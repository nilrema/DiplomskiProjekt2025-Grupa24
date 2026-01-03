import axelrod as axl

C = axl.Action.C 
D = axl.Action.D

def strategy(me, opponent):
    return C if D not in opponent.history else D
    
