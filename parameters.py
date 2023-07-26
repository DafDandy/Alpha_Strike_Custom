short_range = 3
medium_range = 3
long_range = 12
light_mech = 35
medium_mech = 55
heavy_mech = 75
assault_mech = 80
structure_head = 0
structure_ct = 1
structure_torso = 2
structure_arm = 3
structure_legs = 4
armor_calculation_value = 30
pv_calculation = 40

#need to complete the list
ammo_list = ['SRM 6 Ammo', 'SRM 4 Ammo', 'SRM 2 Ammo', 'Machine Gun Ammo', r'AC/20 Ammo', r'AC/10 Ammo', r'AC/5 Ammo', r'AC/2 Ammo']

skill_0 = 1.75
skill_1 = 1.6
skill_2 = 1.4
skill_3 = 1.2
skill_4 = 1
skill_5 = .9
skill_6 = .85

#need to get this part working for error exceptions
def skill_calculation(skill, pv):
    if skill == 0:
        return round(pv * skill_0)
    elif skill == 1:
        return round(pv * skill_1)
    elif skill == 2:
        return round(pv * skill_2)
    elif skill == 3:
        return round(pv * skill_3)
    elif skill == 4:
        return round(pv * skill_4)
    elif skill == 5:
        return round(pv * skill_5)
    elif skill == 6:
        return round(pv * skill_6)


def size(attribute_dictionary):
    if int(attribute_dictionary['Tonnage:']) <= light_mech:
        return 1
    elif int(attribute_dictionary['Tonnage:']) >= light_mech and int(
            attribute_dictionary['Tonnage:']) <= medium_mech:
        return 2
    elif int(attribute_dictionary['Tonnage:']) > medium_mech and int(
            attribute_dictionary['Tonnage:']) < assault_mech:
        return 3
    elif int(attribute_dictionary['Tonnage:']) >= assault_mech:
        return 4

def movement_calculation(movement_dictionary):
    if movement_dictionary['jumping'] == 0:
        return str(movement_dictionary['walking']) + '"'
    elif movement_dictionary['jumping'] == movement_dictionary['walking']:
        return str(movement_dictionary['walking']) + '"'
    elif movement_dictionary['jumping'] >= movement_dictionary['walking'] or movement_dictionary['jumping'] <= \
            movement_dictionary['walking']:
        return str(movement_dictionary['walking']) + '"/' + str(movement_dictionary['jumping']) + '"'

def tmm_calculation(movement_dictionary):
    if movement_dictionary['walking'] <= 8:
        return 1
    elif movement_dictionary['walking'] >= 10 and movement_dictionary['walking'] < 14:
        return 2
    elif movement_dictionary['walking'] >= 14 and movement_dictionary['walking'] < 20:
        return 3
    elif movement_dictionary['walking'] >= 20 and movement_dictionary['walking'] < 24:
        return 4
    elif movement_dictionary['walking'] > 24:
        return 5

def damage_calculation(overheat, short, medium, long):
    if overheat == 2:
        return [0 if i < 0 else i for i in [sum(short), sum(medium) - 1, sum(long) - 1]]
    elif overheat == 3:
        return [0 if i < 0 else i for i in [sum(short) - 2, sum(medium) - 2, sum(long) - 2]]
    elif overheat == 4:
        return [0 if i < 0 else i for i in [sum(short) - 2, sum(medium) - 3, sum(long) - 3]]
    else:
        return [0 if i < 0 else i for i in[sum(short), sum(medium), sum(long)]]

def heatsink_calculation(list_str):
    if len([i for i in list_str if 'Double' in i]) > 1:
        return int([i for i in list_str if 'Heat Sink' in i][0][34:36])
    else:
        return int([i for i in list_str if 'Heat Sink' in i][0][30:32])

def armor_structure_calculation(list_str):
    armor = int([i for i in list_str if 'Armor Factor' in i][0][30:33])

    structure = [[i for i in list_str if 'Head' in i],
                 [i for i in list_str if 'Center Torso' in i],
                 [i for i in list_str if 'R/L Torso' in i],
                 [i for i in list_str if 'R/L Arm' in i],
                 [i for i in list_str if 'R/L Leg' in i]]

    structure = sum([eval(i) for i in[structure[structure_head][0][29:30],
                 structure[structure_ct][0][29:31],
                 structure[structure_torso][0][29:31],
                 structure[structure_arm][0][29:31],
                 structure[structure_legs][0][29:31]]])

    return armor, structure

def ammo_count(ammo_list, list_str):
    for l in ammo_list:
        for i in list_str:
            if l in i:
                return i