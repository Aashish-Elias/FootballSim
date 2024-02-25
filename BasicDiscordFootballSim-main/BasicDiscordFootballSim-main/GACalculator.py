#GA Calculator
import yaml

GoalData = {}
AssistData = {}
GA = {}

with open("GoalTally.yml",'r') as file:
    GoalData = yaml.safe_load(file)
    if GoalData == None:
        GoalData = {}
with open("AssistTally.yml",'r') as file:
    AssistData = yaml.safe_load(file)
    if AssistData == None:
        AssistData = {}