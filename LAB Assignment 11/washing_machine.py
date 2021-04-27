import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

"""
Antecedents (INPUTS)
"""

mClothes = ctrl.Antecedent(np.arange(0,11,1), 'mClothes')
#dirtiness of cloths as dCloths
dCloths = ctrl.Antecedent(np.arange(0,11,1), 'dCloths')

"""
Consequent (OUTPUT)
"""
#washing time as wTime
wTime = ctrl.Consequent(np.arange(0,21,1), 'wTime')

"""
membership functions
"""

mClothes['low_load'] = fuzz.trimf(mClothes.universe, [0,0,4])
mClothes['medium_load'] = fuzz.trimf(mClothes.universe, [1,5,9])
mClothes['full_load'] = fuzz.trimf(mClothes.universe, [6,10,10])

dCloths['not_dirty'] = fuzz.trimf(dCloths.universe, [0,0,3])
dCloths['lightly_dirty'] = fuzz.trimf(dCloths.universe, [2,3,5])
dCloths['medium_dirty'] = fuzz.trimf(dCloths.universe, [4,5,7])
dCloths['very_dirty'] = fuzz.trimf(dCloths.universe, [6,10,10])

wTime['little_time'] = fuzz.trimf(wTime.universe, [0,0,5])
wTime['medium_time'] = fuzz.trimf(wTime.universe, [4,7,10])
wTime['long_time'] = fuzz.trimf(wTime.universe, [9,12,15])
wTime['very_long_time'] = fuzz.trimf(wTime.universe, [14,20,20])

#wTime.view()
"""
fuzzy rules
"""

rule1 = ctrl.Rule( mClothes['full_load'] & dCloths['very_dirty'], wTime['very_long_time'])
rule2 = ctrl.Rule( mClothes['full_load'] & dCloths['medium_dirty'], wTime['very_long_time'])
rule3 = ctrl.Rule( mClothes['full_load'] & dCloths['lightly_dirty'], wTime['long_time'])
rule4 = ctrl.Rule( mClothes['full_load'] & dCloths['not_dirty'], wTime['little_time'])
rule5 = ctrl.Rule( mClothes['medium_load'] & dCloths['very_dirty'], wTime['very_long_time'])
rule6 = ctrl.Rule( mClothes['medium_load'] & dCloths['medium_dirty'], wTime['medium_time'])
rule7 = ctrl.Rule( mClothes['medium_load'] & dCloths['lightly_dirty'], wTime['medium_time'])
rule8 = ctrl.Rule( mClothes['medium_load'] & dCloths['not_dirty'], wTime['little_time'])
rule9 = ctrl.Rule( mClothes['low_load'] & dCloths['very_dirty'], wTime['long_time'])
rule10 = ctrl.Rule( mClothes['low_load'] & dCloths['medium_dirty'], wTime['long_time'])
rule11 = ctrl.Rule( mClothes['low_load'] & dCloths['lightly_dirty'], wTime['little_time'])
rule12 = ctrl.Rule( mClothes['low_load'] & dCloths['not_dirty'], wTime['little_time'])


#rule10.view()
"""
control system
"""
wTime_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12])

washing_time=ctrl.ControlSystemSimulation(wTime_ctrl)
"""
simulation 
"""

# washing_time.input['tClothes'] = 5
# washing_time.input['tDirty'] = 4
# washing_time.input['mClothes'] = 9
# washing_time.input['dCloths'] = 3


print("Enter load of clothes")
washing_time.input['mClothes'] = int(input())
print("Enter dirtiness of clothes")
washing_time.input['dCloths'] = int(input())


washing_time.compute()
print("washing time: ",washing_time.output['wTime'])
wTime.view(sim=washing_time)
plt.show()
mClothes.view(sim=washing_time)
plt.show()
dCloths.view(sim=washing_time)
plt.show()
