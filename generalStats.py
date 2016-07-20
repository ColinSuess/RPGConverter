import sys
def ChangeFDFDotValue(findString,CoDlist):
    indexNumber = 0
    for each in CoDlist:
        try:
            if each.find(findString + ')') > -1:
                CoDlist.insert(indexNumber,'/T(' + findString + ')/V/Yes>>')
                CoDlist.remove(each)
                return
            indexNumber = indexNumber + 1
        except:
            print("exception in ChangeFDFDotValue, your honor!")
            print(sys.exc_info())  
    return

def	ChangeFDFTextValue(TName,replacementText,CoDlist):
    try:
        indexNumber = 0
        for each in CoDlist:
            if each.find(TName + ')') > -1:
                CoDlist.insert(indexNumber,'/T(' + TName + ')/V(' + str(replacementText) + ')>>') #variable
                CoDlist.remove(each)
            indexNumber = indexNumber + 1
    except:
        print("exception in ChangeFDFTextValue, your honor!")
        print(sys.exc_info())  
    return

#defines stats that are calculated regardless of sheet format.
def integrityConverter(alignment,record):
    #This is pretty arbitrary...The assumption is Good and Law both have higher Integrity. Chaos and Evil have lower Integrity. Neutrality sits in the middle.
    #It doesn't hold up to a lot of scrutiny. I could also make the argument that Good and Neutral aren't that different...but...whatever.
    if alignment == 'LG':
        record['Integrity'] = 9
    if alignment == 'NG':
        record['Integrity'] = 8
    if alignment == 'CG':
        record['Integrity'] = 7
    if alignment == 'LN':
        record['Integrity'] = 6
    if alignment == 'N':
        record['Integrity'] = 5
    if alignment == 'CN':
        record['Integrity'] = 4
    if alignment == 'LE':
        record['Integrity'] = 3
    if alignment == 'NE':
        record['Integrity'] = 2
    if alignment == 'CE':
        record['Integrity'] = 1

    return

def sizeConverter(size,record):
    if size == 'Fine':
        record['Size'] = 1
    if size == 'Diminutive':
        record['Size'] = 2
    if size == 'Tiny':
        record['Size'] = 3
    if size == 'Small':
        record['Size'] = 4
    if size == 'Medium':
        record['Size'] = 5
    if size == 'Large':
        record['Size'] = 8
    if size == 'Huge':
        record['Size'] = 20
    if size == 'Gargantuan':
        record['Size'] = 40
    if size == 'Colossal':
        record['Size'] = 60
    return

def acConverter(gear,record):
    if str(gear).find('leather'):
        armor = 1
    if str(gear).find('hide'):
        armor = 1
    if str(gear).find('plate'):
        armor = 3
    if str(gear).find('chain'):
        armor = 1
    if str(gear).find('scale'):
        armor = 2
    if str(gear).find('splint'):
        armor = 2
    if str(gear).find('banded'):
        armor = 2
    if str(gear).find('breast'):
        armor = 2
    if str(gear).find('shield'):
        armor = armor + 1
    if str(gear).find('buckler'):
        armor =  armor + 1
    record['Armor'] = armor

    return

def weaponry(weaponSet): #accepts melee and ranged columns
    weaponSet = weaponSet.split(sep = ',')
    CoDweaponSet = []
    for weapon in weaponSet:
        weapon = weapon.split(sep = '+')
        if len(weapon) < 2:
            weapon = weapon[0].split(sep = '-')
        if weapon[0] == '':
            weapon[0] = weapon[1]
            weapon[1] = weapon[2]
        try:
            if weapon[1].find('1d2') > -1 or weapon[1].find('1d3') > -1 or weapon[1].find('1d4') > -1:
                weapon[1] = 1
            elif weapon[1].find('1d6') > -1 or weapon[1].find('1d8') > -1 or weapon[1].find('2d4') > -1:
                weapon[1] = 2
            elif weapon[1].find('1d10') > -1 or weapon[1].find('1d12') > -1 or weapon[1].find('2d6') > -1:
                weapon[1] = 3
            elif weapon[1].find('2d10') > -1 or weapon[1].find('2d12') > -1:
                weapon[1] = 4
            else:
                    weapon[1] = 5
            CoDweaponSet.append([weapon[0],weapon[1]])
        except IndexError:
            print('there was a problem with weapons at ',record['Name'],', ',weapon)
            pass
        return CoDweaponSet

def CoDAbilityConverter(abilityScore,record):
    try:
        if abilityScore == 0:
            abilityScore = 1
            return abilityScore
        if abilityScore == '':
            abilityScore = 1
            return abilityScore
        try:
            abilityScore = (int(abilityScore) - 10) // 2
        except ValueError:
            abilityScore = 1
        if abilityScore < 1:
            abilityScore = 1
    except:
        abilityScore = 1
        return abilityScore
    return abilityScore

def meritConverter(feats):
    dotMapDictionaryMerits = {
        'merits1':[265,'','',''],
        'merits2':[273,'','',''],
        'merits3':[281,'','',''],
        'merits4':[289,'','',''],
        'merits5':[297,'','',''],
        'merits6':[305,'','',''],
        'merits7':[313,'','',''],
        'merits8':[321,'','',''],
        'merits9':[329,'','','za'],#suffix
        'merits10':[337,'','','za']}
    return

def ChangeFDFWeapons(CoDlist,record): #can probably be leveraged for merits, etc.
#Weapon/Attack Dmg Range Clip Init Str Size
#example CoDweaponSet == [['bite ', 5], [' tail slap ', 3]]
    dotMapWeapons = {'weapon1':['weap/att1','weap/att5','weap/att9','weap/att13','weap/att17','weap/att21','weap/att25'],
        'weapon2':['weap/att2','weap/att6','weap/att10','weap/att14','weap/att18','weap/att22','weap/att26'],
        'weapon3':['weap/att3','weap/att7','weap/att11','weap/att15','weap/att19','weap/att23','weap/att27'],
        'weapon4':['weap/att4','weap/att8','weap/att12','weap/att16','weap/att20','weap/att24','weap/att28']}
    try:
        if record['CofDMelee'] == '' and record['CofDRanged'] == '':
            return
        weaponsList = record['CofDMelee'] + record['CofDRanged']
    except:
        if record['CofDMelee'] == '':
            weaponsList = record['CofDRanged']
        else:
            weaponsList = record['CofDMelee']

    weaponNumber = 0
    
    try:
        for dictItem in dotMapWeapons.items(): #correct loop. Leave it alone.
            selectedWeapon = weaponsList[weaponNumber]
            field = 0
            for every in dictItem[1]:
                TName = every
                ChangeFDFTextValue(every,selectedWeapon[field],CoDlist)
                field = field + 1
            weaponNumber = weaponNumber + 1 #this will always cause an index error...
        return
    except:
        print("exception in ChangeFDFWeapons, your honor!")
        print(sys.exc_info())
        print('placeholder') 

