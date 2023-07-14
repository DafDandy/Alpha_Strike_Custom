import tkinter as tk
from tkinter import filedialog
import pandas as pd
import weapon_dict
pd.set_option('display.max_rows', None)


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

file = open(file_path).read()
list_str = file.split('\n')
list_str = [x for x in list_str if x != '' and len(x)<=60]

attributes = []
weapons = []
values_interest = ['Cost', 'Technology Base', 'Tonnage:', 'Battle Value']
for i in range(len(list_str)):
    for x in values_interest:
        if x in list_str[i]:
            attributes.append(list_str[i][(len(x + ' ')):])

attributes = [s.strip() for s in attributes]
attribute_dictionary = dict(zip(values_interest, attributes))

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


# Creating the weapon dictionary
keys = ['Armament']
dict2 = {x:key_value_pairs[x] for x in keys}
weapons = dict2['Armament'].split(',')

def strip_list_noempty(mylist):
    newlist = (item.strip() if hasattr(item, 'strip') else item for item in mylist)
    return [item for item in newlist if item != '']

weapons = strip_list_noempty(weapons)

weapon_value = []
weapon_key = []
for i in weapons:
    weapon_key.append(i[2:])
    weapon_value.append(i[:1])
weapon_dict = dict(zip(weapon_key, weapon_value))


# Pulling heatsinks for overheat calculation
if len([i for i in list_str if 'Double' in i]) >1:
    heatsinks = [i for i in list_str if 'Heat Sink' in i]
    heatsinks = int(heatsinks[0][34:36])
else:
    heatsinks = [i for i in list_str if 'Heat Sink' in i]
    heatsinks = int(heatsinks[0][30:32])

#  Finding armor points
armor = [i for i in list_str if 'Armor Factor' in i]
armor = int(armor[0][30:33])

structure =[[i for i in list_str if 'Head' in i],
            [i for i in list_str if 'Center Torso' in i],
            [i for i in list_str if 'R/L Torso' in i],
            [i for i in list_str if 'R/L Arm' in i],
            [i for i in list_str if 'R/L Leg' in i]]

structure = [structure[0][0][29:30],
             structure[1][0][29:31],
             structure[2][0][29:31],
             structure[3][0][29:31],
             structure[4][0][29:31]]

structure = sum([eval(i) for i in structure])

#  Calculating the final outputs for the alpha strike card values

armor_rating = round(armor / 30)

if int(attribute_dictionary['Tonnage:']) < 40:
    SZ = 1
elif int(attribute_dictionary['Tonnage:']) >= 40 and int(attribute_dictionary['Tonnage:']) <= 55:
    SZ = 2
elif int(attribute_dictionary['Tonnage:']) >= 60 and int(attribute_dictionary['Tonnage:']) <= 75:
    SZ = 3
elif int(attribute_dictionary['Tonnage:']) >= 80:
    SZ = 4

if movement_dictionary['jumping'] == 0:
    movement = str(movement_dictionary['walking']) + '"'
elif movement_dictionary['jumping'] == movement_dictionary['walking']:
    movement = str(movement_dictionary['walking']) + '"'
elif movement_dictionary['jumping'] >= movement_dictionary['walking'] or movement_dictionary['jumping'] <= \
        movement_dictionary['walking']:
    movement = str(movement_dictionary['walking']) + '"/' + str(movement_dictionary['jumping']) + '"'

if movement_dictionary['walking'] <= 8:
    tmm = 1
elif movement_dictionary['walking'] >= 10 and movement_dictionary['walking'] < 14:
    tmm = 2
elif movement_dictionary['walking'] >= 14 and movement_dictionary['walking'] < 20:
    tmm = 3
elif movement_dictionary['walking'] >= 20 and movement_dictionary['walking'] < 24:
    tmm = 4
elif movement_dictionary['walking'] > 24:
    tmm = 5

print(attribute_dictionary)
print(movement_dictionary)
print(weapon_dict)
print(heatsinks)
print(structure)
print(armor_rating)
print(movement)
print(tmm)