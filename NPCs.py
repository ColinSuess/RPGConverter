import generalStats
import sys

def ChangeFDFEquipment(CoDlist,record): #can probably be leveraged for merits, etc.
#Equipment Durability Structure Size Cost
    #Use this if I ever feel like populating the whole thing
    #dotMapEquipment = {'equipment1':['equip1','equip4','equip7','equip10','equip13'],
    #    'equipment2':['equip2','equip5','equip8','equip11','equip14'],
    #    'equipment3':['equip3','equip6','equip9','equip12','equip15'],
    #    'equipment4':['equip16','equip17','equip18','equip19','equip20']}
    dotMapEquipment = ['equip1','equip2','equip3','equip16']
    
    if str(record['Gear']) == '':
        print(str(record['Gear']) == '')
        return

    equipmentList = record['Gear']
    equipmentList = equipmentList.split(sep = ', ')
    equipmentNumber = 0

    try:
        for item in dotMapEquipment:
            selectedEquipment = equipmentList.pop()
            TName = item
            generalStats.ChangeFDFTextValue(item,selectedEquipment,CoDlist)
        return
    except:
        print("exception in ChangeFDFEquipment, your honor!")
        print(sys.exc_info())
        print('placeholder') 


def abilityExtractor(abilityList,record):

    abilityList = abilityList.split(sep = ',')
    
    for ability in abilityList:
        
        ability = abilityList.pop(0)
        ability = ability.strip()
        ability = ability.replace('-','')
        if ability.find(' ') == -1:
            ability = ability + ' 0'
        abilityList.append(ability)

    for ability in abilityList:
        ability = ability.split(sep = ' ')
        record[ability[0]] = generalStats.CoDAbilityConverter(ability[1],record)
    return

def npcStats(record): #for stats using the NPC .csv file format

    try:
        abilityExtractor(record['AbilityScores'],record)
        record['Brawl'] = int(record['BaseAtk']) // 5
        record['Firearms'] = int(record['BaseAtk']) // 5
        record['Weaponry'] = int(record['BaseAtk']) // 5
        record['Description'] = record['Description']
    except:
        print("exception in NPCs.py, your honor!")
        print(sys.exc_info())
        exit
    return

