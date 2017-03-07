# Udacity Open Street Map Data Wrangling Project
**Zach Dischner, March 07 2017** 

**MongoDB** Backend for the location of **Boulder, CO** 

![Boulder](http://i.imgur.com/FNcm7dS.png)

## Introduction
I chose to examine my home town of Boulder, Colorado with OSM data. It has a good mix of city, farmland, and more rural mountainous terrain. 

Some general stats for the Boulder area:

| Stat | Value |
|---|---|
| Raw OSM File  | 92.3MB |
| Parsed JSON File  | 126MB |
| Number of DB Records<sup>1</sup> | 461568 |
| Number of Nodes<sup>2</sup> | 414901 |
| Number of Ways<sup>3</sup> | 46410 |
| Number of Unique Users<sup>4</sup> | 658 |


## Data Wrangling
Arguably the most time and thought consuming part of this process was extracting and cleaning data from the Open Street Map provided xml product. The following were the main problems addressed during the wrangling phase

#### *Street type abbreviations* - Street type modifiers had little consistency with regards to case, punctuation, and abbreviation. 
I chose to expand all abbreviated street type specifications into capitalized, full length street type specifications. Street types were identified as trailing strings in the address specification that exactly matched one of a hand-defined set of abbreviated or punctuated street types. All punctuation was also removed from the expanded address.

* Ex "2521 w 108th **pl.**" ==> "2521 w 108th **Place**"

#### *Abbreviated directions* - Directions were often abbreviated and had mixed case
Like the street type abbreviations, I replaced lowercase and abbreviated direction specifications (middle of a string and isolated by spaces) with a capitalized, spelled out, and non-punctuated direction. 

* Ex "2521 **w** 108th pl" ==> "2521 **West** 108th pl"

#### *Zip code inconsistencies* - Zipcodes were called post codes, and often had modifiers 
I chose to rename any `addr:postcode` specifications as `zipcode`, and I cleaned up the postcode value so that *modified* zips were excluded, and any extranious information was ommitted such that the end result was always a 5 digit zipcode.  

* Ex "**CO** 80302**-1234**" ==> "80302"

#### *Nested Sections* - Some xml tags behaved like address specifications, with `:` separated subspecifications that seemed relevant enough to parse out. 
I chose to allow arbritrary single-nested subsection specifications to be turned into a nested dictionary/document, just like I did specifically for `addr:subspec` tags. Infinitely recursed subsections are not supported, instead just a single additional subsection document is allowed, with any further subsections just being included with the `:` marker included. 

* Ex "\<tag k="**tiger:county**" v="Weld, CO"/>" "\<tag k="**tiger:name_base**" v="Sycamore"/>" ==> "tiger: {county:"weld", name_base:"Sycamore"}`

## Data Exploration
### Top 10 contributors<sup>5</sup>:
The user *Berjoh* has nearly 80000 contributions, which is nearly twice what the next highest contributor has. The boxplot below illustrates this disparity, with a span of the top 10 Boulder area contributors called out

|User|Contributions|
|---|---|
|Berjoh|79645|
|mattchn|40409|
|woodpeck_fixbot|38552| 
|GPS_dr|36462|
|ColoSean|32108|
|Rub21|27281|
|oddityoverseer|22137|
|bobmc|17618|
|Stevestr|10628|
|ddk6|9655|

![Imgur](http://i.imgur.com/4RmxTtb.png)

### Least Active Contributors<sup>6</sup>
106 users have contributed only 1 post, which is just 0.133% of the top user's contribution.


## Appendix A - Reference Queries
See the exploratory code in `mongoMapExplore.py` for actual queries ran. Below are nearly identical reproductions of each query for reference. 
Precursor:

```python
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client.get_database("OpenStreetMap")
boulder = db.get_collection("Boulder")
```

1. `boulder.count()`
2. `boulder.find({"type":"node"}).count()`
3. `boulder.find({"type":"way"}).count()`
4. `len(boulder.distinct('created.user'))`
5. `boulder.aggrigate([{"$group":  {"_id":"$created.user", "contribs":{"$sum":1} } },{"$sort":{"contribs":-1} },{"$limit":  10}])`
6. 
















