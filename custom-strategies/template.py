import axelrod as axl

C = axl.Action.C  # C stands for cooperate
D = axl.Action.D  # D stands for defect


def strategy(me, opponent):
    # 'me' and 'opponent' are Player classes from the axelrod library

    # You can use your and your opponents history
    # history is just a list of axl.Action objects
    myHistory = me.history
    oppHistory = opponent.history

    # your logic will calculate your response
    # here we just set the response to "defect" for demonstration purposes

    if not myHistory:
        # here you can set your response if this is the first round of the game
        # e.g let's cooperate first
        response = D
    else:
        # here you can set your response if you have some knowledge of the previous rounds
        # e.g let's just set the response then to "defect"
        response = D

    return response
