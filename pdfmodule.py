
import csv
import io
import sys
import time

def restoreFDFContent(listOfContent):
    restoredString = '<<'
    popper = 0
    length = len(CoDlist)
    while popper < length:
        if len(restoredString) > 2:
            restoredString = restoredString + '<<'
        tempCoDlistitem = CoDlist.pop(0)
        restoredString = restoredString + tempCoDlistitem
        popper = popper + 1

    outputFile = io.open('output.txt','w')
    outputFile.writelines(restoredString)
    outputFile.close()

def importTable(importedTable):

    with io.open('NPCDBcsv2.csv',encoding='latin-1') as importedFile:
        readlineResults = importedFile.readline()
        keys = [readlineResults.split(sep=',')]

        reader = csv.DictReader(importedFile,keys[0])
        for row in reader:
            importedTable.append(row)

def abilityExtractor(abilityList):

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
        record[ability[0]] = abilityConverter(ability[1])
    return

def abilityConverter(abilityScore):
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

def skillExtractor(skillList):

    completeSkillList = ['Acrobatics','Appraise','Bluff','Climb','Craft','Diplomacy','Disable Device','Disguise','Escape Artist','Fly','Handle Animal','Heal','Intimidate','Knowledge (arcana)','Knowledge (dungeoneering)','Knowledge (engineering)','Knowledge (geography)','Knowledge (history)','Knowledge (local)','Knowledge (nature)','Knowledge (nobility)','Knowledge (planes)','Knowledge (religion)','Linguistics','Perception','Perform','Profession','Ride','Sense Motive','Sleight of Hand','Spellcraft','Stealth','Survival','Swim','Use Magic Device']
    for skill in completeSkillList:    
        record[skill] = 0

    skillList = skillList.split(sep = ',')

    while len(skillList) > 0:
        
        skill = skillList.pop(0)
        skill = skill.replace(" ' ",'')
        skill = skill.strip("]")
        skill = skill.replace("[",'')
        skill = skill.replace("'",'')
        skill = skill.strip("'")
        skill = skill.strip()
        if skill.find('+') == -1:
            continue
        else:
            skill = skill.split(sep = '+')

        record[skill[0].strip()] = skillConverter(skill[0].strip(),skill[1])

    return

def skillConverter(skillName,skillScore):
    skillScore = 0
    if skillName.find('Know'):
        skillScore = skillScore - abilityConverter(record['Int'])
    elif skillName == 'Bluff' or 'Diplomacy' or 'Disguise' or 'Handle Animal' or 'Intimidate' or 'Perform' or 'Use Magic Device':
        skillScore = skillScore - abilityConverter(record['Cha'])
    elif skillName == 'Acrobatics' or 'Disable Device' or 'Escape Artist' or 'Fly' or 'Ride' or 'Sleight of Hand' or 'Stealth':
        skillScore = skillScore - abilityConverter(record['Dex'])
    elif skillName == 'Heal' or 'Perception' or skillName.find('Profession') or 'Sense Motive' or 'Survival':
        skillScore = skillScore - abilityConverter(record['Wis'])
    elif skillName == 'Appraise' or skillName.find('Craft') or 'Linguistics' or 'Spellcraft':
        skillScore = skillScore - abilityConverter(record['Int'])
    elif skillName == 'Climb' or 'Swim':
        skillScore = skillScore - abilityConverter(record['Str'])

    if skillScore > 16:
        skillScore = 5
    elif skillScore > 12:
        skillScore = 4
    elif skillScore > 8:
        skillScore = 3
    elif skillScore > 4:
        skillScore = 2
    else: skillScore = 1

    return skillScore

def integrityConverter(alignment):
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
    initialFindLength = len(CoDlist[0])
    indexNumber = 0
    for each in CoDlist:
        integrityFindString = '(integdot',record.get('Integrity'),')'
        if each.find(integrityFindString) > -1 and len(each) != initialFindLength:
            initialFindLength = len(each)
            CoDlist.insert(indexNumber,'/T(','integrityFindString',')/V/Yes>>')
            CoDlist.remove(each)
            print(each)
        indexNumber = indexNumber + 1
    return

def sizeConverter(size):
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

def acConverter(gear):
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
    CofDweaponSet = []
    for weapon in weaponSet:
        weapon = weapon.split(sep = '+')
        if len(weapon) < 2:
            weapon = weapon[0].split(sep = '-')
        if weapon[0] == '':
            weapon[0] = weapon[1]
            weapon[1] = weapon[2]
        try:
            if weapon[1].find('�') > -1 or weapon[1].find('1d2') > -1 or weapon[1].find('1d3') > -1 or weapon[1].find('1d4') > -1:
                weapon[1] = 1
            elif weapon[1].find('1d6') > -1 or weapon[1].find('1d8') > -1 or weapon[1].find('2d4') > -1:
                weapon[1] = 2
            elif weapon[1].find('1d10') > -1 or weapon[1].find('1d12') > -1 or weapon[1].find('2d6') > -1:
                weapon[1] = 3
            elif weapon[1].find('2d10') > -1 or weapon[1].find('2d12') > -1:
                weapon[1] = 4
            else:
                weapon[1] = 5
            CofDweaponSet.append([weapon[0],weapon[1]])
        except IndexError:
            print('there was a problem with weapons at ',record['Name'],', ',weapon)
            pass
        
        
    return CofDweaponSet

#Start kinda-perf counter
totalTime = 0
timerStart = time.clock()


CoDfdf = io.open('CofD_1-Page_Interactive_test_fdf.fdf')

CoDlist = []

CoDlist = CoDfdf.readlines()

CoDlist = CoDlist[2].split(sep = '<<')

try:
    importedTable = []

    importTable(importedTable)



    for record in importedTable:
        try:        

            abilityExtractor(record['AbilityScores'])
            skillExtractor(record['Skills'])
            integrityConverter(record['Alignment'])

            record['Intelligence'] = abilityConverter(record['Int'])
            record['Wits'] = abilityConverter(record['Wis'])
            record['Resolve'] = abilityConverter(record['Wis'])
            record['Strength'] = abilityConverter(record['Str'])
            record['Dexterity'] = abilityConverter(record['Dex'])
            record['Stamina'] = abilityConverter(record['Con'])
            record['Presence'] = abilityConverter(record['Cha'])
            record['Manipulation'] = abilityConverter(record['Cha'])
            record['Composure'] = abilityConverter(record['Wis'])

            record['Athletics'] = record['Acrobatics']
            record['Brawl'] = int(record['BaseAtk']) // 5
            record['Drive'] = record['Ride']
            record['Firearms'] = int(record['BaseAtk']) // 5
            record['Larceny'] = record['Sleight of Hand']
            record['Stealth'] = record['Stealth'] # overwrites value
            record['Survival'] = record['Survival'] # overwrites value
            record['Weaponry'] = int(record['BaseAtk']) // 5
            record['Animal Ken'] = record['Knowledge (nature)']
            record['Empathy'] = record['Sense Motive']
            record['Expression'] = abilityConverter(record['Cha'])
            record['Intimidation'] = record['Intimidate']
            record['Persuasion'] = record['Diplomacy']
            record['Socialize'] = record['Diplomacy']
            record['Streetwise'] = record['Knowledge (local)']
            record['Subterfuge'] = record['Bluff']
            record['Academics'] = record['Knowledge (history)']
            record['Computer'] = abilityConverter(record['Int'])
            record['Crafts'] = abilityConverter(record['Int'])
            record['Investigation'] = record['Appraise']
            record['Medicine'] = record['Heal']
            record['Occult'] = record['Knowledge (arcana)']
            record['Politics'] = record['Knowledge (nobility)']
            record['Science'] = record['Knowledge (engineering)']
            record['Natural Philosophy'] = record['Knowledge (engineering)']
            record['Exoterica'] = record['Knowledge (religion)']
            record['Description'] = record['Description']
            sizeConverter(record['Size'])
            record['Health'] = record['Stamina'] + record['Size']
            record['Willpower'] = record['Composure'] + record['Resolve']
            record['Speed'] = record['Strength'] + record['Dexterity'] + 5
            #Weird defense math wuxia (lowest of Dexterity or Wits) = Athletics
            defenseAttribute = record['Dexterity']
            if record['Wits'] > defenseAttribute:
                defenseAttribute = record['Wits']      
            record['Defense'] = record['Athletics'] + defenseAttribute
            try:
                acConverter(record['OtherGear'])
            except:
                pass
            record['Initiative'] = record['Dexterity'] + record['Composure']
            if record['Melee'] != '':
                record['CofDMelee'] = weaponry(record['Melee'])
            else:
                record['CofDMelee'] = ''
            if record['Ranged'] != '':
                record['CofDRanged'] = weaponry(record['Ranged'])
            else:
                record['CofDRanged'] = ''

        except:
            continue

    CoDCSV = open('CoDCSV.csv','w',newline='')
    CoDwriter = csv.DictWriter(CoDCSV,importedTable[0].keys(),'','ignore')
    CoDwriter.writeheader()

    ValueErrors = 0
    UnicodeEncodeErrors = 0
    for record in importedTable:
        try:
            CoDwriter.writerow(record)
        except UnicodeError:
            UnicodeEncodeErrors = UnicodeEncodeErrors + 1
            pass
        except ValueError:
            ValueErrors = ValueErrors + 1
            pass

    print('ValueErrors',ValueErrors)
    print('UnicodeEncodeErrors',UnicodeEncodeErrors)
    CoDCSV.close()
    
    

except:
    print("exception, your honor!")
    print(sys.exc_info())
    exit

finally:
        
    timerEnd = time.clock()
    totalTime = totalTime + timerEnd - timerStart
    print("Total time: ",totalTime)


print(CoDlist)

restoreFDFContent(CoDlist)

print('HOLD SINNER')