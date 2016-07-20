def select(record):
    try:    
        int(record['BaseAtk']) > 0
        FDF = 'CofD_1-Page_Interactive_blank.fdf'
        
        #future feature is shunt caster classes into MTA_2ndED_4-Pagev2_Interactive.fdf
        casterClasses = ['Bard',
                        'Alchemist',
                        'Inquisitor',
                        'Magus',
                        'Investigator',
                        'Skald',
                        'Mesmerist',
                        'Occultist',
                        'Spiritualist',
                        'Warpriest',
                        'Kineticist',
                        'Paladin',
                        'Ranger',
                        'Summoner',
                        'Bloodrager',
                        'Medium',
                        'Cleric',
                        'Druid',
                        'Sorcerer',
                        'Wizard',
                        'Oracle',
                        'Witch',
                        'Arcanist',
                        'Shaman',
                        'Psychic']
        for each in casterClasses:
            if record['Class'].find(each) > -1:
                FDF = 'MTA_2ndED_2-Pagev2_Interactive.fdf'
                return FDF
    except KeyError:
        FDF = 'CofD_Horrors_1-Page_Interactive.fdf'
        return FDF
    except:
        print("exception, your honor!")
        print(sys.exc_info())
    return FDF

    #except KeyError:
    #    if str(record['Subtype']).casefold() == str('incorporeal').casefold():
    #        FDF = 'CofD_GodMachine_EphemeralBeings_1-Page_Interactive.fdf'
    #    else:
    #        FDF = 'CofD_Horrors_1-Page_Interactive.fdf'
    #    return FDF

