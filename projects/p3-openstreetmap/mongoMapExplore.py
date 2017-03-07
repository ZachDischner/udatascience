#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__     = 'Zach Dischner'                      
__copyright__  = "NA"
__credits__    = ["NA"]
__license__    = "NA"
__version__    = "0.0.1"
__maintainer__ = "Zach Dischner"
__email__      = "zach.dischner@gmail.com"
__status__     = "Dev"
__doc__        ="""
File name: mongoMapUtils.py
Created:  Mar/01/2017
Modified: Mar/06/2017

Parse open street map data, downloaded from https://www.openstreetmap.org. Data comes downloaded as an osm (xml) file.
Cleaned elements of the dataset are saved to a json file for import into a MongoDB database. 

Some initial data problems:
    * Addresses use "postcode" not "zipcode"
    * Zipcodes sometimes have supplimental specifications
    * Streettypes all over the place

Problems to discuss:
    * LASP is wrong, neat 1950 Colorado Ave, should be 1234 Innovation Drive

Parsing and cleaning functionality is as follows:


"""

##############################################################################
#                             Imports/Definitions
#----------*----------*----------*----------*----------*----------*----------*
import sys
import os
import re
import json
import seaborn as sns
import pandas as pd
from pymongo import MongoClient


###### Organization
_here  = os.path.dirname(os.path.realpath(__file__))  #p3 project directory
_OSMFILE = os.path.join(_here, "mapdata.osm")
_JSONFILE = _OSMFILE + ".json"

###### Database
client = MongoClient('mongodb://localhost:27017')
_MAPDB = "OpenStreetMap"
_COLLECTION = "Boulder"
db = client.get_database(_MAPDB)
collection = db.get_collection(_COLLECTION)


##############################################################################
#                         Data Input Functions
#----------*----------*----------*----------*----------*----------*----------*
def load_data(datafile=_JSONFILE, db=_MAPDB, collection=_COLLECTION):
    """Simple, just run the command line utility"""
    ret = os.system(f"mongoimport --db {db} --collection {collection} --file {datafile}")
    print(f"Finished importing {datafile} into database {db}, collection {collection} with status code {ret}")


##############################################################################
#                          DB Query Functions
#----------*----------*----------*----------*----------*----------*----------*
# nodes = [n for n in collection.find({"created.user":"GPS_dr"}).limit(5)]
def tableprint(header,values):
    """Simple list of dictionaries to markdown table"""
    print("|" + "|".join(header) + "|")
    print("|---"*(len(header)) + "|")
    for vdict in values:
        for item in vdict.values():
            print(f"|{item}", end="")
        print("|")

def print_summary():
    num = collection.count()
    nodes = collection.find({"type":"node"}).count()
    ways = collection.find({"type":"way"}).count()
    num_users = len(collection.distinct('created.user'))
    print(f"| Number of DB Records<sup>1</sup> | {num} |")
    print(f"| Number of Nodes<sup>2</sup> | {nodes} |")
    print(f"| Number of Ways<sup>3</sup> | {ways} |")
    print(f"| Number of Unique Users<sup>4</sup> | {num_users} |")

def print_user_stats():
    ###### Look at top users
    users = collection.aggregate([{"$group":  {"_id":"$created.user", "contribs":{"$sum":1} } },
                            {"$sort":   {"contribs":-1} },
                            # {"$limit":  10}
                            ])
    users = [u for u in users]
    top_user = users[0]
    print(f"Top contributing user is {top_user['_id']} with {top_user['contribs']} contributions")
    tableprint(["User","Contributions"], users)
    
    ## Quick plot
    sns.plt.figure()
    df = pd.DataFrame(users)
    ax = sns.boxplot(x=df['contribs'])
    for _,row in df.iloc[::3].iterrows():
        ax.text(row['contribs']+1000,-0.01, row['_id'])

    ###### Look at how many have posted just one post
    ugroups = collection.aggregate([{"$group":  {"_id":"$created.user", "contribs":{"$sum":1} } },
                                  {"$group":    {"_id":"$contribs", "contrib_groups":{"$sum":1} } },
                                  {"$sort":     {"_id":1} },
                                #   {"$limit":    1}
                                    ])
    ugroups = [ug for ug in ugroups]
    single_group = ugroups[0]["contrib_groups"]
    print(f"\n{single_group} users have contributed only 1 post\nwhich is just {single_group/top_user['contribs']*100:3.3f}% of the top user's contribution")

    return ugroups, users

def print_node_types():


def main():
    print_summary()
    print_user_stats()
    print_node_types


##############################################################################
#                              Runtime Execution
#----------*----------*----------*----------*----------*----------*----------*
if __name__ == "__main__":
    print(f"Parsing Open Street Map Data from {_OSMFILE}")
    ret = main(input_file=_OSMFILE, output_file=_JSONFILE, parse_every=_PARSE_EVERY)
    print(f"Finished parsing every {_PARSE_EVERY} elemet from {_OSMFILE}. Output saved to {_JSONFILE} ")
    sys.exit(0)