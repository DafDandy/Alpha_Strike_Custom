import tkinter as tk
from tkinter import filedialog
from collections import Counter
import time
import parameters
import weapon_dict as wp
import math
import parameters as pm
import re

# print("Please select your mech sheet that you wish to convert into an alpha strike card at the prompt...")
# time.sleep(2)

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

file = open(file_path).read()

skill = int(input("Enter your skill level between 0 and 6: "))

list_str = file.split('\n')
list_str = [x for x in list_str if x != '' and len(x)<=60]

attributes = []
weapons = []
values_interest = ['Technology Base', 'Tonnage:', 'Battle Value']
for i in range(len(list_str)):
    for x in values_interest:
        if x in list_str[i]:
            attributes.append(list_str[i][(len(x + ' ')):])

attributes = [s.strip() for s in attributes]
attribute_dictionary = dict(zip(values_interest, attributes))

if 'Clan' in attributes[0]:
    tech = 'clan'
else:
    tech = 'inner'

# Movement dict creation and calculation
movement_substr = [i for i in list_str if 'MP' in i]
movement_value = [i * 2 for i in ([int(movement_substr[0][13:15]),int(movement_substr[2][13:15])])]
movement_key = ['walking', 'jumping']
movement_dictionary = dict(zip(movement_key, movement_value))

# Grabbing the cost elements
key_value_pairs = {}
current_key = None

lines = file.split('\n')
for line in lines:
    line = line.strip()
    if line:
        if ':' in line:
            current_key, value = line.split(':', 1)
            key_value_pairs[current_key.strip()] = value.strip()
        elif current_key is not None:
            if current_key == 'Armaments':
                if current_key not in key_value_pairs:
                    key_value_pairs[current_key] = line.strip()
                else:
                    key_value_pairs[current_key] += f', {line.strip()}'
            else:
                key_value_pairs[current_key] += f', {line.strip()}'

def strip_list_noempty(mylist):
    newlist = (item.strip() if hasattr(item, 'strip') else item for item in mylist)
    return [item for item in newlist if item != '']

if tech == 'inner':
    # Creating the weapon dictionary for inner sphere
    keys = ['Armament']
    dict2 = {x:key_value_pairs[x] for x in keys}
    weapons = dict2['Armament'].split(',')

    weapons = strip_list_noempty(weapons)

    weapon_value = []
    weapon_key = []
    for i in weapons:
        weapon_key.append(i[2:])
        weapon_value.append(i[:1])

    weapon_key = [x.replace(' ', '_').replace('/', '__').replace('-', '__') for x in weapon_key]

    weapon_dict = dict(zip(weapon_key, weapon_value))

if tech == 'clan':
    keys = ['Left Arm Actuators']
    dict2 = {x:key_value_pairs[x] for x in keys}
    weapons = dict2['Left Arm Actuators'].split(',')

    weapons = strip_list_noempty(weapons)[4:]
    weapon_key = []
    weapon_value = []
    for i in weapons:
        weapon_key.append(i[:26].strip())

    weapon_key = [x.replace(' ', '_').replace('/', '__').replace('-', '__') for x in weapon_key]
    weapon_dict = dict(Counter(weapon_key))



#  Calculating the final outputs for the alpha strike card values

heat = []
for x,y in weapon_dict.items():
    if hasattr(wp, x):
       heat.append((int(getattr(wp, x)[1]) * int(y)))

short = []
medium = []
long = []
for x,y in weapon_dict.items():
    if hasattr(wp, x):
        if getattr(wp, x)[3] <= pm.short_range or getattr(wp, x)[2] <= pm.short_range:
            short.append(round(float(getattr(wp, x)[0]) * int(y)))
        if getattr(wp, x)[4] > pm.medium_range:
            medium.append(round(float(getattr(wp, x)[0]) * int(y)))
        if getattr(wp, x)[5] > pm.long_range:
            long.append(round(float(getattr(wp, x)[0]) * int(y)))

# Final calculations
if tech == 'inner':
    pv = round(int(attribute_dictionary['Battle Value'].replace(',', '')) / pm.pv_calculation_is)
if tech == 'clan':
    pv = round(int(attribute_dictionary['Battle Value'].replace(',', '')) / pm.pv_calculation_clan)

armor, structure = parameters.armor_structure_calculation(list_str)

if tech == 'inner':
    heatsinks = parameters.heatsink_calculation_is(list_str)
if tech == 'clan':
    heatsinks = parameters.heatsink_calculation_clan(list_str)

overheat = math.ceil(sum(heat)/heatsinks)

if tech == 'inner':
    damage = parameters.damage_calculation_is(overheat, short, medium, long)
if tech == 'clan':
    damage = parameters.damage_calculation_clan(overheat, short, medium, long)



pv = parameters.skill_calculation(skill, pv)

armor_rating = round(armor / pm.armor_calculation_value)

size = parameters.size(attribute_dictionary)

movement = parameters.movement_calculation(movement_dictionary)

tmm = parameters.tmm_calculation(movement_dictionary)

# ammo = parameters.ammo_count(parameters.ammo_list, list_str)

print("Sending HPG message to Comstar...")
time.sleep(2)

print("Message received!"
      "\n"
      "Peace of Blake be with you"
      "\n")
print("Mech: " + list_str[0])
print("PV: " + str(pv))
print("Movement: " + str(movement))
print("TMM: " + str(tmm))
print("Size: " + str(size))
if tech == 'inner':
    print("Armament: " + str(weapons))
if tech == 'clan':
    print("Armament: " + str(weapon_dict))
print("Overheat: " + str(overheat))
print("Structure: " + str(math.floor(structure/10)))
print("Armor: " + str(armor_rating))
print("Damage Bracket: " + str(damage))

print("""\n
\n
Conversion Complete!""")

# end = input(" \nPressing Enter twice will end transmission")

