import axelrod as axl 
import matplotlib.pyplot as plt

# needed for createPlayer function
import importlib.util
import os
import sys

class CustomPlayer(axl.Player):
    def __init__(self, name, decisionFunction):
        super().__init__()
        self.name = name
        self.foo = decisionFunction

    def strategy(self, opponent):
        return self.foo(self, opponent)

    def __str__(self):
        return self.name

def createPlayer(name, filePath):
    fileName = list(filePath.split('/'))[-1]
    fullPath = os.path.abspath(filePath)
    moduleName = os.path.splitext(fileName)[0]
    spec = importlib.util.spec_from_file_location(moduleName, fullPath)
    
    if spec is None:
        raise FileNotFoundError(f"Could not find the file {moduleName}")

    module = importlib.util.module_from_spec(spec)
    
    sys.modules[moduleName] = module
    spec.loader.exec_module(module)
    strategy = module.strategy
    strategy.__name__ = name
    return CustomPlayer(name, strategy) 





# testing
# templatePlayer = createPlayer("template", "../custom-strategies/template.py")
# players = [axl.Cooperator(), axl.Alternator(), axl.Defector(), axl.TitForTat(), templatePlayer]
#
# tournament = axl.Tournament(players, turns=100, repetitions=3)
# results = tournament.play()
# print(results.ranked_names)
# plot = axl.Plot(results)
# p = plot.boxplot()
# plt.show()




