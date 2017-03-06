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
File name: mapDataParser.py
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
import xml.etree.cElementTree as ET
import re
import codecs
import json

###### Organization
_here  = os.path.dirname(os.path.realpath(__file__))  #p3 project directory
_OSMFILE = os.path.join(_here, "mapdata.osm")
_JSONFILE = _OSMFILE + ".json"
_PARSE_EVERY = 10

###### Parsing Definitions
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

## Will get augmented by a function below to be all regexy
_STREET_MAPPING = { "St": "Street",
            "Ave":"Avenue",
            "Av":"Avenue",
            "Rd":"Road",
            "Blvd":"Boulevard",
            "Brdwy":"Broadway",
            "Ln":"Lane",
            "Tr":"Trail",
            "Dr":"Drive",
            "Cm":"Commons",
            "Com":"Commons",
            "Cr":"Circle",
            "Pl":"Place",
            "Pkwy":"Parkway",
            "Pkway":"Parkway",
            "Ct":"Court",
            "Sq":"Square",
            "Wy":"Way",
            "Pt":"Point"
            }
_DIR_MAPPING = {"N":"North", "E":"East", "W":"West", "S":"South"}

###### Utils
## Colors!!!
class bcolors:
    HEADER  = '\033[95m'
    OKBLUE  = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'

def printColor(msg,color):
    print(color + str(msg) + bcolors.ENDC)

def printYellow(msg):
    printColor(msg,bcolors.WARNING)
def printGreen(msg):
    printColor(msg,bcolors.OKGREEN)
def printBlue(msg):
    printColor(msg, bcolors.OKBLUE)
def printRed(msg):
    printColor(msg,bcolors.FAIL)

##############################################################################
#                         XML Parsing Functions
#----------*----------*----------*----------*----------*----------*----------*
def _get_elements(fname,tags):
    """Unlimited generator that yield element if it is the right type of tag

    Reference:
    http://effbot.org/zone/element-iterparse.htm 
    """
    ## Get an iterable, turn it into an iterator
    context = iter(ET.iterparse(fname, events=('start', 'end')))
    _, root = next(context)

    ## Iterate over elements
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear() ## Need to clear the root, otherwise we will get a huge list of empty children I guess

def get_elements(osm_file=_OSMFILE, tags=( 'node','way', 'relation'), limit=None):
    """Safe, count limited generator to get `limit` elements from an xml document which match `tags`

    Basically a safety wrapper for `_get_elements` so we don't go throuh a whole huge document for testing. 
    """
    count = 0
    element_generator = _get_elements(osm_file,tags)
    while True:
        yield next(element_generator)
        if limit is not None:
            count += 1
            if count > limit: return

##############################################################################
#                         Data Cleaning Functions
#----------*----------*----------*----------*----------*----------*----------*
def _augment_re_mapping(orig_mapping):
    """This gets called on import
    
    Reference:
        http://stackoverflow.com/questions/6713310/how-to-specify-space-or-end-of-string-and-space-or-start-of-string"""
    def findme(x):
        return f"(?<!\S){x}(?!\S)"
    mapping = {}
    for k,v in orig_mapping.items():
        mapping[findme(k)] = v
        mapping[findme(k+".")] = v
        mapping[findme(k.lower())] = v
        mapping[findme(k.upper())] = v
        
        # Also include the destination mapping as a key, in all cases
        mapping[findme(v)] = v
        mapping[findme(v.lower())] = v
        mapping[findme(v.upper())] = v
    
    # Alphabetically sort for convenience if you wantsorted(m.keys(), key=lambda s:s.lower()):
    return mapping

def expand_from_mapping(to_expand, mapping):
    
    ###### Try each pattern (key in mapping) agains the string we want to expand
    for pattern,map_to in mapping.items():
        m = re.search(pattern, to_expand)
        if m:
            ## Found our pattern. Substitute with the expanded mapping and return
            return re.sub(pattern, map_to, to_expand)
    ## Pattern wasn't found, return original string
    return to_expand

def expand_streettype(addr_string):
    # print(f"\nSearching for street type pattern in '{street}'")
    return expand_from_mapping(addr_string, STREET_MAPPING)

def expand_streetdir(addr_string):
    return expand_from_mapping(addr_string, DIR_MAPPING)

def parse_zip(key,value):
    """Parse and check on zipcode specification. Return new spec and value after it has been verified and Cleaned
    """
    ## Rename
    spec="zipcode"

    ## Extract 5 digit zipcode. EG could be "CO 80302-1334"
    truezip = re.findall("(\d{5})($|-)",value) # Search for two matches. Just care about the first one
    if truezip:
        value = truezip[0][0]
    else:
        printYellow(f"\nZipcode field is not understood! Key:{key}=Value:{value}. Flagging as unknown")
        return spec, "UNKNOWN-"+value

    if not value.startswith("8"):
        printYellow(f"\nZipcode field does not appear to be in Boulder! Key:{key}=Value:{value}. Adding anyways")
    
    return spec,value


##############################################################################
#                         Main Parsing Flow Functions
#----------*----------*----------*----------*----------*----------*----------*
def parse_attributes(element):
    """parse Attriburtes out of an XML element
    EG:
        <xmlelement attrib1='foo' attrib2='bar'... >"""
    node = {}
    ## Start by adding all XML element attributes to node dictionary.
    # element.attrib is a straight up dictionary of all attributes 
    node.update(element.attrib)

    ## Try to extract lat/lon. These attributes go into an array field called "pos"
    try:
        node["pos"] = [float(node.pop("lat")), float(node.pop("lon"))]
    except:
        pass

    ## Created information. CREATED information should go in a nested dictionary called "created'"
    created_elements = [(k,node.pop(k)) for k in CREATED if node.get(k)]
    if created_elements:
        node['created'] = dict(created_elements)
    return node

def parse_children(element):
    """Parse children of an element (only tags for now)"""
    attrs = {}
    subdicts = {}
    for child in element.getchildren():
        ## Tag parsing
        if child.tag == "tag":
            try: 
                key = child.attrib['k']
                value = child.attrib['v']
            except:
                key,value = child.attrib.items[0]
            
            ## 1. Check for problematic characters
            if re.search(problemchars, key):
                continue
    
            ## 3. Parse out "addr:something"
            if key.startswith("addr:"):
                ## 2. Ignore any key with multiple : specifiers
                if len(key.split(":")) > 2:
                    print(f"ignoring nested address info: {key}")
                    continue
                addr,spec = key.split(":")
                # Replace "postcode" with "zipcode", check if it seems valid. Only really works for Boulder, CO, USA
                if spec=="postcode": 
                    spec,value = parse_zip(key,value)

                if spec=="street": 
                    # print(f"Street found: {spec}={value}")
                    value = expand_streettype(value)
                    value = expand_streetdir(value)
                if "address" not in subdicts: subdicts["address"] = {}
                subdicts["address"].update({spec:value})

            ## 4. Anything else with ":" subspecifications which we'll break in to subdicts/subdocuments
            elif len(key.split(":")) > 1:
                *classifier,spec = key.split(":")                
                ## Accommodate another level of nested values. AKA "service:bicycle:pump"
                # Too lazy to figure out a quick infinite subclassifier (infinitely many ':'s and accompanying subdictionaries)
                #   unknown value added for the time sink and potential for increased processing time. 
                if len(classifier) > 1:
                    if len(classifier) >= 2:
                        # print(f"\n\t\tMore than two nested ':' encountered in Key:{key} Value:{value}. Just adding as is and continuing")
                        attrs[key] = value
                        continue
                    subc,subspec = classifier
                    if subc not in subdicts: subdicts[subc] = {}
                    if subspec not in subdicts[subc]: subdicts[subc][subspec] = {}
                                        
                    try:
                        subdicts[subc][subspec].update({spec:value})
                    except:
                        try:
                            ## Sometimes we have duplicated values
                            subdicts[subc][subspec] = [subdicts[subc][subspec][spec]] + [value] 
                        except:
                            print(f"\n\t\tProblem1 parsing {key}={value}! subdicts:{subdicts}, subc:{subc}, subspec:{subspec}, spec:{spec}")
                else:
                    classifier = classifier[0]
                    if classifier not in subdicts: subdicts[classifier] = {}
                    try:
                        subdicts[classifier].update({spec:value})
                    except:
                        print(f"\n\t\tProblem2 parsing {key}={value}! subdicts:{subdicts}, classifier:{classifier}, spec:{spec}")
            else:
                attrs[key] = value
        elif child.tag == "nd":
            if "node_refs" not in attrs: attrs['node_refs'] = []
            attrs['node_refs'].append(child.attrib['ref'])

    attrs.update(subdicts)
    return attrs

def parse_element(element):
    node = {}
    node['type'] = element.tag
    attrs = parse_attributes(element)
    child_attrs = parse_children(element)
    node.update(attrs)
    node.update(child_attrs)
    return node



##############################################################################
#                         Program Flow Functions
#----------*----------*----------*----------*----------*----------*----------*

def main(input_file=_OSMFILE, output_file=_JSONFILE, parse_every=_PARSE_EVERY,pretty=False, samplesize=1000):
    sample = {}
    with codecs.open(output_file, "w") as fo:
        for ii, element in enumerate(get_elements(input_file)):
            if ii % parse_every == 0:
                print(f"\rParsing {ii}th element: {element.tag}", end="")
                parsed = parse_element(element)
                if pretty:
                    fo.write(json.dumps(parsed, indent=2)+"\n")
                else:
                    fo.write(json.dumps(parsed) + "\n")
                if len(sample) < samplesize:
                    sample.update({parsed['id']:{"parsed":parsed,"element":element}})
        print(f"Parsed {ii/parse_every} elements from {input_file}")
    return sample
                

STREET_MAPPING = _augment_re_mapping(_STREET_MAPPING)
DIR_MAPPING = _augment_re_mapping(_DIR_MAPPING)

##############################################################################
#                              Runtime Execution
#----------*----------*----------*----------*----------*----------*----------*
if __name__ == "__main__":
    print(f"Parsing Open Street Map Data from {_OSMFILE}")
    ret = main(input_file=_OSMFILE, output_file=_JSONFILE, parse_every=_PARSE_EVERY)
    print(f"Finished parsing every {_PARSE_EVERY} elemet from {_OSMFILE}. Output saved to {_JSONFILE} ")
    sys.exit(0)