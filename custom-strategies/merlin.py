import axelrod as axl

C = axl.Action.C  # C stands for cooperate
D = axl.Action.D  # D stands for defect


# cautious optimist
def strategy(me, opponent):
    if not me.history:
        return C

    cooperation_rate = opponent.history.cooperations / len(opponent.history)
    return C if cooperation_rate > 0.6 else D

    # ========
    # jos dvije strategije dolje
    #
    # streak breaker
    # def strategy(me, opponent):
    if not me.history:
        return C

    if len(opponent.history) >= 3 and opponent.history[-3:] == [C, C, C]:
        return D
    if len(opponent.history) >= 2 and opponent.history[-2:] == [D, D]:
        return D

    return C

    # mindfucker
    # def strategy(me, opponent):
    if not me.history:
        return C

    opponent_defections = opponent.history.defections
    my_recent_defections = (
        me.history[-opponent_defections:].count(D)
        if len(me.history) >= opponent_defections
        else 0
    )

    if my_recent_defections < opponent_defections:
        return D

    return C
