import generalStats
def monsterStats(record): #for stats using the monster .csv file format
    creatureType = {'aberration':1.5,
                    'animal':1.5,
                    'construct':1,
                    'dragon':1,
                    'fey':2,
                    'humanoid':1.5,
                    'magical beast':1,
                    'monstrous humanoid':1,
                    'ooze':1.5,
                    'outsider':1.5,
                    'plant':1.5,
                    'undead':1.5,
                    'vermin':1.5}
    try:
        HD = str(record['HD'])
        HD = HD.strip(')(')
        HD = HD.split(sep='d')
        HD = int(HD[0])
        if HD > 24: #Need to exercise this code path.
            HD = 24
    except:
        print('error in monsters')
        return
    record['Brawl'] = HD // int(creatureType.get(record['Type'].casefold())) // 5
    record['Firearms'] = HD // 5
    record['Weaponry'] = HD // 5
    record['Description'] = ''

    abilityList = ['Str','Dex','Con','Int','Wis','Cha']
    for ability in abilityList:
        record[ability] = generalStats.CoDAbilityConverter(record[ability],record)
    return
