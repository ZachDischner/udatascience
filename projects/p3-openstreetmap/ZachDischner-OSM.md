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
106 users have contributed only 1 post, which is just 0.133% of the top user's contribution. I find it notable that the vast majority of the contributions come from a smaller demographic of dedicated users. 

## Additional Exploration: Amenities
Particular interest here is in what services and amenities are marked in Boulder. For these statistics, nodes and ways were both considered, amenities fell into both categories.

The top 10 most occuring amenities are shown in the table below. Not surprisingly as one who lives here and commutes everywhere is the fact that bike parking is listed as the second most common amenity. Boulder is regularly ranked as one of the most biker friendly cities in the country https://matadornetwork.com/trips/8-bike-friendly-cities-america/. Within city limits, Boulder has 431<sup>8</sup> marked bikeways. 

**Top 10 Amenities in Boulder, CO**<sup>7</sup>

|Amenity/Service Type|Count in Boulder|
|---|---|
|parking|1194|
|bicycle_parking|646|
|restaurant|223|
|bench|174|
|school|104|
|fast_food|100|
|cafe|93|
|place_of_worship|76|
|bank|55|
|fuel|50|

### Religion
Boulder is a mix of college town and wealthy and educated working population, dominated by mostly politically left-leaning caucasians [Wiki](https://en.wikipedia.org/wiki/Boulder,_Colorado#Demographics). I was curious about whether or not the distribution of places of worship would reflect these trends. Christian institutions dominate the landscape here, followed by "Unknown" denominations. From experience, there are a number of atypical religious groups around the area. However, a quick examination at the "Unknown" places of worship<sup>11</sup> seems to indicate that it is more likely that these locations simply weren't classified as belonging to a particular denomination.
 
**Top 5 places of worship in Boulder, CO**<sup>9</sup>

|Place of Worship|Count in Boulder|
|---|---|
|christian|59|
|Unknown|12|
|jewish|2|
|unitarian_universalist|2|
|muslim|1|

### Cuisine
Boulder is also known to be a foodie town ([Wiki](https://en.wikipedia.org/wiki/Boulder,_Colorado#Top_rankings)). At the same time, it is indeed part college town with nearly 1/3 of it's population hailing from the University of Colorado. The first and second most numerous food types are "Unknown" and "Pizza", respectively. A town with an abundance of pizza offerings immediately fits the bill for a college town. Additionally, a quick examination of the "Unknown" cuisines<sup>12</sup> implies that these restaurants are simply uncategorized because they often fall outside of easily identifiable cuisine classifications. This supports, or at least fails to reject, the idea that Boulder is indeed a foodie town. These are observations only, especially since the OSM dataset is uncontrolled and contains a lot of irregularaties. However the trends observed do seem to match the expected demographic behavior.

**Top 10 Cuisine Types of worship in Boulder, CO**<sup>10</sup>

|Cuisine|Count in Boulder|
|---|---|
|Unknown|76|
|pizza|16|
|chinese|15|
|mexican|15|
|italian|10|
|american|8|
|sandwich|8|
|sushi|8|
|breakfast|7|
|indian|7|

## Ideas for Future Study
### Cross-City Comparison
The trends identified so far are made only with reference to Boulder's OSM dataset. It would be helpful to compare these stats to other cities, to see if Boulder really does have more bikeways than the average city, or if there are more or fewer churches in this proclaimed left-wing town. 

### Route/Distance Computation
Additionally, I would like to look into total bikeable distance, and average distance of bikeable "cycleways". The approach here would be to look at the lat/lon of associated nodes along a way, tracked by the `node_ref` array, and calculate path length as of an *open* way. That investigation is more involved, and will be left for another exersize. 

### Densities
Finally, examining the densities of certain amenities or nodes with respect to lat/lot in order to guestimate the *hotspots* in Boulder. One could select all nodes in a grid defined by lat/lons, and then sort the locations by highest density of noders. As a prototype, getting all nodes between 40 and 41 degrees latitude, -106 and -105 degrees longitude would look like this: `nodes = boulder.find({"pos.0":{"$lt":41,"$gt":40}, "pos.1":{"$lt":-105,"$gt":-104}}`. Doing this type of search and grouping directly in MongoDB would be preferrable, but again I'll leave this to another investigation

## Appendix A - Reference Queries
See the exploratory code in `mongoMapExplore.py` for actual queries ran. Below are nearly identical reproductions of each query for reference. 
Precursor:

```python
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client.get_database("OpenStreetMap")
collection = db.get_collection("Boulder")
boulder = collection # for convenience
```

1. `boulder.count()`
2. `boulder.find({"type":"node"}).count()`
3. `boulder.find({"type":"way"}).count()`
4. `len(boulder.distinct('created.user'))`
5. `boulder.aggrigate([{"$group":  {"_id":"$created.user", "contribs":{"$sum":1} } },{"$sort":{"contribs":-1} },{"$limit":  10}])`
6. `collection.aggregate([{"$group":  {"_id":"$created.user", "contribs":{"$sum":1} } },
                                  {"$group":    {"_id":"$contribs", "contrib_groups":{"$sum":1} } },
                                  {"$sort":     {"_id":1} },
                                  {"$limit":    1}
                                    ])`
7. `boulder.([{"$match":   {"amenity": {"$exists":True}}},
                                        {"$group":  {"_id":     "$amenity", "count":{"$sum":1}}},
                                        {"$sort":   {"count":-1}}
                                      ])`
8. `boulder.find({"type":"way", "highway":"cycleway"}).count()`   
9. `boulder.aggregate([{"$match":   {"amenity": {"$exists":True}, "amenity":"place_of_worship"}},
                                    {"$group":  {"_id":     "$religion", "count":{"$sum":1}}},
                                    {"$sort":   {"count":-1}}
                                      ])`
10. `collection.aggregate([{"$match":   { "amenity": {"$exists":True}, "amenity":"restaurant"}},
                                    {"$group":  {"_id":     "$cuisine", "count":{"$sum":1}}},
                                    {"$sort":   {"count":-1}}
                                      ])`                               
11. `[_ for _ in boulder.find({"amenity":"place_of_worship","religion":{"$exists":False}})]`
12. `[_ for _ in boulder.find({"amenity":"restaurant","cuisine":{"$exists":False}})]`


## Appendix B - Document Structure
Since MongoDB is schemaless, there is no set structure that describes every document. However they do have a general form, illustrated by the example below. 

**Node**:

```json
{'_id': ObjectId('58bd9a614645d0fbde114702'),
 'address': {'housenumber': '627',
             'street': 'South Broadway',
             'zipcode': '80305'},
 'amenity': 'pub',
 'created': {'changeset': '42390292',
             'timestamp': '2016-09-23T21:05:09Z',
             'uid': '21931',
             'user': 'amm',
             'version': '8'},
 'id': '25782064',
 'name': 'Southern Sun',
 'opening_hours': 'Mo-We 16:00-01:00; Th-Su 11:30-01:00',
 'phone': '3035430886',
 'pos': [39.9842183, -105.2493081],
 'type': 'node',
 'website': 'http://www.southernsunpub.com'}
```

**Way**:

```json
{'_id': ObjectId('58bd9a694645d0fbde179f91'),
 'created': {'changeset': '7569770',
             'timestamp': '2011-03-15T20:13:35Z',
             'uid': '117055',
             'user': 'GPS_dr',
             'version': '2'},
 'highway': 'service',
 'id': '17015643',
 'node_refs': ['1203544554',
               '1203542626',
               '1203543427',
               '1203543406',
               '176389889',
               '176389891'],
 'service': 'alley',
 'tiger': {'cfcc': 'A41',
           'county': 'Boulder, CO',
           'reviewed': 'no',
           'separated': 'no',
           'source': 'tiger_import_dch_v0.6_20070809',
           'tlid': '188245474:188244953',
           'upload_uuid': 'bulk_upload.pl-1b7afdac-0ecb-47b2-8901-e595d422ff1f'},
 'type': 'way'}
```















