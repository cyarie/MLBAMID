"""
This is all pretty straight-forward: MLBAM uses JSON data to store biographical information on all active and historical MLB -- and, apparently, more -- players,
and then use JavaScript and other webmagic to serve that information up on the MLB website. As of this script's creation, MLBAM IDs start at 110001 with Hank Aaron,
and end at 624589 with... someone. The script pretty much crawls through every biographical JSON file served up by MLB's website, and pulls out the first name, last name,
and birthdate info, which should make it pretty easy to sync up with the Lahman Database. It will need some occasional tweaking at the season goes along and players
are added to the MLBAM ID database.

I use Pandas to stick the dictionary into a formatted and readable dataframe, which makes exporting to CSV easy and accurate. The dataframe is indexed to the player's
MLBAM ID.

Should really eventually include more error handling, just in case my list of IDs is inaccurate -- this is the first real and useful Python/programming thing I have ever
done, so I'm getting around to figuring out how to do that.
"""

import urllib2
import json
import pandas as pd
from pandas import Series, DataFrame

""" Establishes the known minimum and maximum MLBAM IDs. Max will change as the season goes along. """
KNOWN_MIN = 110001
KNOWN_MAX = 624589

""" Uses the min and max MLBAM IDs to build a list of all known MLBAM IDs """
idList = [x for x in range(KNOWN_MIN, KNOWN_MAX + 1)]

""" 
Where the magic happens. Takes in the list of MLBAM IDs, scrapes JSON data, and returns a massive dictionary containing all the relevant data, which bioDict being
a dictionary of biographical information, keyed to the player's MLBAM ID.
"""
def scrape_players(list):
    baseURL = "http://mlb.com/lookup/json/named.player_info.bam?sport_code=%27mlb%27&player_id="
    playerDict = {}
    bioDict = {}
    for playerID in list:
        realURL = baseURL + str(playerID)
        playerJSON = json.load(urllib2.urlopen(realURL), encoding='latin-1')
        playerName = playerJSON['player_info']['queryResults']['row']['name_display_first_last']
        playerName = playerName.split()
        nameFirst = playerName[0]
        nameLast = playerName[1]
        playerBirth = playerJSON['player_info']['queryResults']['row']['birth_date']
        playerBirth = playerBirth.split('T')
        playerBirth = playerBirth[0].split('-')
        try:
            birthYear = playerBirth[0]
            birthMonth = playerBirth[1]
            birthDay = playerBirth[2]
        except IndexError:
            birthYear = 'null'
            birthMonth = 'null'
            birthDay = 'null'
        bioDict = {'nameFirst': nameFirst, 'nameLast': nameLast, 'birthYear': birthYear, 'birthMonth': birthMonth, 'birthDay': birthDay}
        playerDict[playerID] = bioDict
    return(DataFrame.from_dict(playerDict, orient="index"))

idFrame = scrape_players(idList[0:10])
print idFrame
idFrame.to_csv('test.csv')