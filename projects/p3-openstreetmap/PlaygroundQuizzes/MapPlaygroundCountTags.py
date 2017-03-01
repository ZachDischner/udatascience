###### 1 XML parsing with tags and children
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    def update_tags(root):
        tags[root.tag] = (tags.get(root.tag) or 0) + 1
        for child in root.getchildren():
            if child.tag:
                tags[child.tag] = (tags.get(child.tag) or 0) + 1
                for subchild in child.getchildren():
                    print "Subchild: ",subchild
                    update_tags(subchild)
            else:
                print "No child.tag"
                continue
        
    tags = {}
    tree = ET.parse(filename)
    root = tree.getroot()
    update_tags(root)

    return tags
    


def test():

    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

    

if __name__ == "__main__":
    test()

## XML string
"""  
    <?xml version="1.0" encoding="UTF-8"?>
<osm version="0.6" generator="CGImap 0.3.3 (28791 thorn-03.openstreetmap.org)" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">
 <bounds minlat="41.9704500" minlon="-87.6928300" maxlat="41.9758200" maxlon="-87.6894800"/>
 <node id="261114295" visible="true" version="7" changeset="11129782" timestamp="2012-03-28T18:31:23Z" user="bbmiller" uid="451048" lat="41.9730791" lon="-87.6866303"/>
 <node id="261114296" visible="true" version="6" changeset="8448766" timestamp="2011-06-15T17:04:54Z" user="bbmiller" uid="451048" lat="41.9730416" lon="-87.6878512"/>
 <node id="261114299" visible="true" version="5" changeset="8581395" timestamp="2011-06-29T14:14:14Z" user="bbmiller" uid="451048" lat="41.9729565" lon="-87.6939548"/>
 <node id="261146436" visible="true" version="5" changeset="8581395" timestamp="2011-06-29T14:14:14Z" user="bbmiller" uid="451048" lat="41.9707380" lon="-87.6976025"/>
 <node id="261147304" visible="true" version="7" changeset="8581395" timestamp="2011-06-29T14:14:15Z" user="bbmiller" uid="451048" lat="41.9740068" lon="-87.6988576"/>
 <node id="261224274" visible="true" version="5" changeset="8581395" timestamp="2011-06-29T14:14:14Z" user="bbmiller" uid="451048" lat="41.9707656" lon="-87.6938669"/>
 <node id="293816175" visible="true" version="47" changeset="8448766" timestamp="2011-06-15T16:55:37Z" user="bbmiller" uid="451048" lat="41.9730154" lon="-87.6890403"/>
 <node id="305896090" visible="true" version="37" changeset="15348240" timestamp="2013-03-13T07:46:29Z" user="Umbugbene" uid="567034" lat="41.9749225" lon="-87.6891198"/>
 <node id="317636974" visible="true" version="12" changeset="15348240" timestamp="2013-03-13T08:02:56Z" user="Umbugbene" uid="567034" lat="41.9740292" lon="-87.7012430"/>
 <node id="317636971" visible="true" version="13" changeset="15348240" timestamp="2013-03-13T08:08:01Z" user="Umbugbene" uid="567034" lat="41.9740556" lon="-87.6979712"/>
 <node id="317637399" visible="true" version="2" changeset="14927972" timestamp="2013-02-05T22:43:49Z" user="Umbugbene" uid="567034" lat="41.9705609" lon="-87.7012048"/>
 <node id="317637398" visible="true" version="2" changeset="14927972" timestamp="2013-02-05T22:43:49Z" user="Umbugbene" uid="567034" lat="41.9706972" lon="-87.7012109"/>
 <node id="365214872" visible="true" version="3" changeset="8448766" timestamp="2011-06-15T17:04:54Z" user="bbmiller" uid="451048" lat="41.9731130" lon="-87.6847998"/>
 <node id="261299091" visible="true" version="6" changeset="8581395" timestamp="2011-06-29T14:14:15Z" user="bbmiller" uid="451048" lat="41.9747482" lon="-87.6988886"/>
 <node id="261114294" visible="true" version="6" changeset="8448766" timestamp="2011-06-15T17:04:54Z" user="bbmiller" uid="451048" lat="41.9731219" lon="-87.6841979"/>
 <node id="261210804" visible="true" version="4" changeset="3359748" timestamp="2009-12-13T00:36:09Z" user="woodpeck_fixbot" uid="147510" lat="41.9707217" lon="-87.7000019"/>
 <node id="261221422" visible="true" version="7" changeset="8581395" timestamp="2011-06-29T14:14:15Z" user="bbmiller" uid="451048" lat="41.9748542" lon="-87.6922652"/>
 <node id="261221424" visible="true" version="7" changeset="8581395" timestamp="2011-06-29T14:14:15Z" user="bbmiller" uid="451048" lat="41.9758794" lon="-87.6923639">
  <tag k="highway" v="traffic_signals"/>
 </node>
 <node id="261198953" visible="true" version="6" changeset="8581395" timestamp="2011-06-29T14:14:13Z" user="bbmiller" uid="451048" lat="41.9707413" lon="-87.6963097"/>
 <node id="757860928" visible="true" version="2" changeset="5288876" timestamp="2010-07-22T16:16:51Z" user="uboot" uid="26299" lat="41.9747374" lon="-87.6920102">
  <tag k="amenity" v="fast_food"/>
  <tag k="cuisine" v="sausage"/>
  <tag k="name" v="Shelly's Tasty Freeze"/>
 </node>
  <way id="258219703" visible="true" version="1" changeset="20187382" timestamp="2014-01-25T02:01:54Z" user="linuxUser16" uid="1219059">
  <nd ref="2636086179"/>
  <nd ref="2636086178"/>
  <nd ref="2636086177"/>
  <nd ref="2636086176"/>
  <tag k="highway" v="service"/>
 </way>
 <relation id="1557627" visible="true" version="2" changeset="14326854" timestamp="2012-12-19T05:32:37Z" user="fredr" uid="939355">
  <member type="node" ref="1258927212" role="via"/>
  <member type="way" ref="110160127" role="from"/>
  <member type="way" ref="34073105" role="to"/>
  <tag k="restriction" v="only_right_turn"/>
  <tag k="type" v="restriction"/>
 </relation>
</osm>
"""