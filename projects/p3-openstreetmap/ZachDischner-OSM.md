# Udacity Open Street Map Data Wrangling Project
**Zach Dischner, March 07 2017** 

**MongoDB** Backend for the location of **Boulder, CO** 

![Boulder](http://i.imgur.com/FNcm7dS.png)

## Introduction
I chose to examine my home town of Boulder, Colorado with OSM data. It has a good mix of city, farmland, and more rural mountainous terrain. 

Stats for the area:

Stat | Value
Raw OSM Size | 100

| Stat | Value |
|---|---|
| Raw OSM File  | 92.3MB |
| Parsed JSON File  | 126MB |
| Number of DB Records<sup>1</sup>| 461568 | 



## Appendix A - Supporting Queries
Precursor:

```python
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client.get_database("OpenStreetMap")
collection = db.get_collection("Boulder")
```

1. `collection.count()`
















