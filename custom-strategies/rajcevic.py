import axelrod as axl

C = axl.Action.C  # C stands for cooperate
D = axl.Action.D  # D stands for defect


def strategy(me, opponent):
    myHistory = me.history
    oppHistory = opponent.history

    if not myHistory:
        response = C
    else:
        matches_played = len(oppHistory)

        if matches_played >= 2:
            no_cooperation = oppHistory[-1] == D and oppHistory[-2] == D
            if no_cooperation:
                response = D
            else:
                response = D if myHistory[-1] == C and myHistory[-2] == C else C

        else:
            response = D

    return response
