"""
Remaining major features before testing:
1. Very basic GUI
2. Take command line inputs


"""
import csv
import io
import sys
import time
import argparse
import selectFDF
import NPCs
import generalStats
import monsters

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
    return restoredString    

def importTable(importedTable,sourceFile):

    with io.open(sourceFile,encoding='latin-1') as importedFile:
        readlineResults = importedFile.readline()
        keys = [readlineResults.split(sep=',')]

        reader = csv.DictReader(importedFile,keys[0])
        for row in reader:
            importedTable.append(row)


def skillExtractor(skillList):
    completeSkillList = ['Acrobatics','Appraise','Bluff','Climb','Craft','Diplomacy','Disable Device','Disguise','Escape Artist','Fly','Handle Animal','Heal','Intimidate','Knowledge (arcana)','Knowledge (dungeoneering)','Knowledge (engineering)','Knowledge (geography)','Knowledge (history)','Knowledge (local)','Knowledge (nature)','Knowledge (nobility)','Knowledge (planes)','Knowledge (religion)','Linguistics','Perception','Perform','Profession','Ride','Sense Motive','Sleight of Hand','Spellcraft','Stealth','Survival','Swim','Use Magic Device']
    for skill in completeSkillList:
        try:
            if record[skill] == '0': 
                record[skill] = 0
                
        except KeyError:
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
        #while skill.find('+') > -1:
        if skill.find('+') == -1:
            continue
        else:
            skill = skill.split(sep = '+')
        skill[0] = skill[0].strip()
        skill[1] = skill[1].replace("(","")
        skill[1] = skill[1].strip()

        if skill[0] in record:
            record[skill[0].strip()] = skillConverter(skill[0].strip(),int(skill[1]))
    

    return

def skillConverter(skillName,skillScore):
    #skillScore = 0
    if skillName.find('Know') > -1:
        skillScore = skillScore - record['Int']
    elif skillName == 'Bluff' or 'Diplomacy' or 'Disguise' or 'Handle Animal' or 'Intimidate' or skillName.find('Perform') > -1 or 'Use Magic Device':
        skillScore = skillScore - record['Cha']
    elif skillName == 'Acrobatics' or 'Disable Device' or 'Escape Artist' or 'Fly' or 'Ride' or 'Sleight of Hand' or 'Stealth':
        skillScore = skillScore - record['Dex']
    elif skillName == 'Heal' or 'Perception' or skillName.find('Profession') > -1 or 'Sense Motive' or 'Survival':
        skillScore = skillScore - record['Wis']
    elif skillName == 'Appraise' or skillName.find('Craft') > -1 or 'Linguistics' or 'Spellcraft':
        skillScore = skillScore - record['Int']
    elif skillName == 'Climb' or 'Swim':
        skillScore = skillScore - record['Str']

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


#Start kinda-perf counter
totalTime = 0
timerStart = time.clock()




try:

    arguementParser = argparse.ArgumentParser()
    arguementParser.add_argument('-src', type=str, default='d20pfsrd-Bestiary-test.csv', help='the source data file with location.')
    arguementParser.add_argument('-fdf', type=str, default='.\\NPCs\\CofD_Horrors_1-Page_Interactive_test.fdf', help='the source FDF file with location. Remember that the FDF looks for its source PDF in the relative path you used to create the FDF.')
    arguementParser.add_argument('-dst', type=str, default='CoDCSV.csv', help='the new destination file name with location. Beware of permission limitations.')
    arguementParser.add_argument('-npc', type=str, default='no', help='use if you want NPC format instead of Horrors. No arguments/parameters.')
    arguementParser.add_argument('-include', type=str, default='all', help='list any systems you want to allow. Automatically forbids the other systems.')
    arguementParser.add_argument('-exclude', type=str, default='', help='list any systems you want to forbid.')
    parsedArgs = arguementParser.parse_args()
    
    print(parsedArgs.npc)

    importedTable = []

    importTable(importedTable,parsedArgs.src)

    for record in importedTable:

        if parsedArgs.fdf != '':
            CoDfdf = io.open(parsedArgs.fdf)
        else:
            CoDfdf = io.open(selectFDF.select(record))
        try:
            CoDfdfList = CoDfdf.readlines()
        except: #Still too fragile for bad input
            print("Exception in CoDfdfList = CoDfdf.readlines()")
            CoDfdf = io.open(selectFDF.select(record))
            CoDfdfList = CoDfdf.readlines()

        CoDlist = []
        CoDlist = CoDfdfList[2].split(sep = '<<')

        try:        
            #These lines work, so... roll back if you need, but they're literal values so they don't allow user-defined values
            #if CoDlist[2].find('/F(CofD_1-Page_Interactive.pdf)') > -1 or CoDlist[2].find('/F(MTA_2ndED_2-Pagev2_Interactive.pdf)') > -1:
            #    NPCs.npcStats(record)
            #elif CoDlist[2].find('CofD_Horrors_1-Page_Interactive.pdf') > -1:
            #    monsters.monsterStats(record)
            
            if parsedArgs.npc == 'yes':
                NPCs.npcStats(record)
            else:
                monsters.monsterStats(record)




            record['Intelligence'] = record['Int']
            record['Wits'] = record['Wis']
            record['Resolve'] = record['Wis']
            record['Strength'] = record['Str']
            record['Dexterity'] = record['Dex']
            record['Stamina'] = record['Con']
            record['Presence'] = record['Cha']
            record['Manipulation'] = record['Cha']
            record['Composure'] = record['Wis']


            skillExtractor(record['Skills'])



            record['Athletics'] = record['Acrobatics']
            record['Larceny'] = record['Sleight of Hand']
            record['Stealth'] = record['Stealth'] # overwrites value
            record['Survival'] = record['Survival'] # overwrites value
            record['Drive'] = record['Ride']
            record['Animal Ken'] = record['Knowledge (nature)']
            record['Empathy'] = record['Sense Motive']
            record['Expression'] = record['Manipulation'] #Needs an actual conversion
            record['Intimidation'] = record['Intimidate']
            record['Persuasion'] = record['Diplomacy']
            record['Socialize'] = record['Diplomacy']
            record['Streetwise'] = record['Knowledge (local)']
            record['Subterfuge'] = record['Bluff']
            record['Academics'] = record['Knowledge (history)']
            record['Computer'] = record['Intelligence']
            record['Crafts'] = record['Intelligence'] #Needs an actual conversion
            record['Investigation'] = record['Appraise']
            record['Medicine'] = record['Heal']
            record['Occult'] = record['Knowledge (arcana)']
            record['Politics'] = record['Knowledge (nobility)']
            record['Science'] = record['Knowledge (engineering)']
            record['Natural Philosophy'] = record['Knowledge (engineering)']
            record['Exoterica'] = record['Knowledge (religion)']

            generalStats.integrityConverter(record['Alignment'],record)
            generalStats.sizeConverter(record['Size'],record)
            record['Health'] = record['Stamina'] + record['Size']
            if record['Health'] > 12:
                 record['Health'] = 12 # or record it in another field
            record['Willpower'] = record['Composure'] + record['Resolve']
            record['Speed'] = record['Strength'] + record['Dexterity'] + 5
            #Weird defense math wuxia (lowest of Dexterity or Wits) = Athletics
            defenseAttribute = record['Dexterity']
            if record['Wits'] > defenseAttribute:
                defenseAttribute = record['Wits']      
            record['Defense'] = record['Athletics'] + defenseAttribute
            try:
                generalStats.acConverter(record['OtherGear'],record)
            except: #need to be specific about my exceptions here...
                pass
            record['Initiative'] = record['Dexterity'] + record['Composure']
            if record['Melee'] != '':
                record['CofDMelee'] = generalStats.weaponry(record['Melee'])
            else:
                record['CofDMelee'] = ''
            if record['Ranged'] != '':
                record['CofDRanged'] = generalStats.weaponry(record['Ranged'])
            else:
                record['CofDRanged'] = ''

            generalStats.ChangeFDFWeapons(CoDlist,record)


            generalStats.ChangeFDFDotValue('willdot' + str(record.get('Willpower')),CoDlist)
            generalStats.ChangeFDFDotValue('hdot' + str(record.get('Health')),CoDlist)
            generalStats.ChangeFDFDotValue('integdot' + str(record.get('Integrity')),CoDlist)

            generalStats.ChangeFDFTextValue('armor',record['Armor'],CoDlist)
            generalStats.ChangeFDFTextValue('size',record['Size'],CoDlist)
            generalStats.ChangeFDFTextValue('name',record['Name'],CoDlist)
            try:
                generalStats.ChangeFDFTextValue('IM',record['Init'],CoDlist)
            except KeyError:
                generalStats.ChangeFDFTextValue('IM',record['Dexterity'],CoDlist)
            generalStats.ChangeFDFTextValue('defense',record['Defense'],CoDlist)
            generalStats.ChangeFDFTextValue('speed',record['Speed'],CoDlist)
            #form [first Dot,second first dot for dots > 5, any needed prefix, any needed suffix
            #Always take the prefix, only take the suffix on [1].  So item[2,0] versus item[2,1,3]
            dotMapDictionary = {'Intelligence':[1,1,'','as'],#suffix
                'Wits':[9,497,'',''],
                'Resolve':[17,505,'',''],
                'Strength':[25,513,'',''],
                'Dexterity':[33,521,'',''],
                'Stamina':[41,529,'',''],
                'Presence':[49,537,'',''],
                'Manipulation':[57,545,'',''],
                'Composure':[65,553,'',''],
                'Academics':[73,562,'',''],
                'Computer':[81,570,'',''],
                'Crafts':[89,578,'',''],
                'Investigation':[97,586,'',''],
                'Medicine':[105,594,'',''],
                'Occult':[113,602,'',''],
                'Politics':[121,610,'',''],
                'Science':[129,615,'',''],
                'Athletics':[137,620,'',''],
                'Brawl':[145,625,'',''],
                'Drive':[153,630,'',''],
                'Firearms':[161,635,'',''],
                'Larceny':[169,1,'DPDot',''], #prefix
                'Stealth':[177,6,'DPDot',''],
                'Survival':[185,11,'DPDot',''],
                'Weaponry':[193,16,'DPDot',''],
                'Animal Ken':[201,21,'DPDot',''],
                'Empathy':[209,26,'DPDot',''],
                'Expression':[217,31,'DPDot',''],
                'Intimidate':[225,36,'DPDot',''],
                'Persuasion':[233,41,'DPDot',''],
                'Socialize':[241,46,'DPDot',''],
                'Streetwise':[249,51,'DPDot',''],
                'Subterfuge':[257,56,'DPDot','']}

            try:
                for dictItem in dotMapDictionary.items():
                    if record[dictItem[0]] > 0:
                        targetDot = dictItem[1][0] + record[dictItem[0]] - 1 #-1 adjusts to the fact that the dictItem[1] would double-add (if record == 2 dots, dictItem makes it 3 dots, which is wrong).
                        targetPhrase = 'dot' + str(targetDot)
                        generalStats.ChangeFDFDotValue(targetPhrase,CoDlist)
            except:
                print("exception for dictItem, your honor!")
                print(sys.exc_info())

            if CoDfdfList[2].find('CofD_1-Page_Interactive') > -1:
                NPCs.ChangeFDFEquipment(CoDlist,record)

            CoDfdfList[2] = restoreFDFContent(CoDlist)
            outputFileName = 'NPCs\\' + str(record['Name']) + '.fdf'

            print(outputFileName)
            outputFile = io.open(outputFileName,'w',errors='ignore')
            outputFile.writelines(CoDfdfList)
            outputFile.close()
        except KeyError:
            continue
        except:
            print("exception for the whole loop, your honor!")
            print(sys.exc_info())
            print('placeholder!')


    if parsedArgs.dst != '':
        destinationFileName = parsedArgs.dst
    else:
        destinationFileName = 'CoDCSV.csv'
    destinationFile = open(destinationFileName,'w',newline='')
    CoDwriter = csv.DictWriter(destinationFile,importedTable[0].keys(),'','ignore')
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
    destinationFile.close()
    
    

except:
    print("exception, your honor!")
    print(sys.exc_info())
    exit

finally:
        
    timerEnd = time.clock()
    totalTime = totalTime + timerEnd - timerStart
    print("Total time: ",totalTime)





print('HOLD SINNER. Successfully got to the last statement in the program.')