#!/usr/bin/env python
"""
$push is similar to $addToSet. The difference is that rather than accumulating only unique values 
it aggregates all values into an array.

Using an aggregation query, count the number of tweets for each user. In the same $group stage, 
use $push to accumulate all the tweet texts for each user. Limit your output to the 5 users
with the most tweets. 
Your result documents should include only the fields:
"_id" (screen name of user), 
"count" (number of tweets found for the user),
"tweet_texts" (a list of the tweet texts found for the user).  

Please modify only the 'make_pipeline' function so that it creates and returns an aggregation 
pipeline that can be passed to the MongoDB aggregate function. As in our examples in this lesson, 
the aggregation pipeline should be a list of one or more dictionary objects. 
Please review the lesson examples if you are unsure of the syntax.

Your code will be run against a MongoDB instance that we have provided. If you want to run this code 
locally on your machine, you have to install MongoDB, download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.

Please note that the dataset you are using here is a smaller version of the twitter dataset used in 
examples in this lesson. If you attempt some of the same queries that we looked at in the lesson 
examples, your results will be different.
"""

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$group"   : {"_id":"$user.screen_name",
                               "count": {"$sum":1},
                               "tweet_texts": {"$push":"$text"}}},
                {"$sort"    :{"count":-1}},
                {"$limit"   :5}
            ]
    return pipeline

def aggregate(db, pipeline):
    return [doc for doc in db.twitter.aggregate(pipeline)]


if __name__ == '__main__':
    db = get_db('twitter')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    import pprint
    pprint.pprint(result)
    assert len(result) == 5
    assert result[0]["count"] > result[4]["count"]
    sample_tweet_text = u'Take my money! #liesguystell http://movie.sras2.ayorganes.com'
    assert result[4]["tweet_texts"][0] == sample_tweet_text
    

###### Tweet Document Structure
# {
#     "_id" : ObjectId("5304e2e3cc9e684aa98bef97"),
#     "text" : "First week of school is over :P",
#     "in_reply_to_status_id" : null,
#     "retweet_count" : null,
#     "contributors" : null,
#     "created_at" : "Thu Sep 02 18:11:25 +0000 2010",
#     "geo" : null,
#     "source" : "web",
#     "coordinates" : null,
#     "in_reply_to_screen_name" : null,
#     "truncated" : false,
#     "entities" : {
#         "user_mentions" : [ ],
#         "urls" : [ ],
#         "hashtags" : [ ]
#     },
#     "retweeted" : false,
#     "place" : null,
#     "user" : {
#         "friends_count" : 145,
#         "profile_sidebar_fill_color" : "E5507E",
#         "location" : "Ireland :)",
#         "verified" : false,
#         "follow_request_sent" : null,
#         "favourites_count" : 1,
#         "profile_sidebar_border_color" : "CC3366",
#         "profile_image_url" : "http://a1.twimg.com/profile_images/1107778717/phpkHoxzmAM_normal.jpg",
#         "geo_enabled" : false,
#         "created_at" : "Sun May 03 19:51:04 +0000 2009",
#         "description" : "",
#         "time_zone" : null,
#         "url" : null,
#         "screen_name" : "Catherinemull",
#         "notifications" : null,
#         "profile_background_color" : "FF6699",
#         "listed_count" : 77,
#         "lang" : "en",
#         "profile_background_image_url" : "http://a3.twimg.com/profile_background_images/138228501/149174881-8cd806890274b828ed56598091c84e71_4c6fd4d8-full.jpg",
#         "statuses_count" : 2475,
#         "following" : null,
#         "profile_text_color" : "362720",
#         "protected" : false,
#         "show_all_inline_media" : false,
#         "profile_background_tile" : true,
#         "name" : "Catherine Mullane",
#         "contributors_enabled" : false,
#         "profile_link_color" : "B40B43",
#         "followers_count" : 169,
#         "id" : 37486277,
#         "profile_use_background_image" : true,
#         "utc_offset" : null
#     },
#     "favorited" : false,
#     "in_reply_to_user_id" : null,
#     "id" : NumberLong("22819398300")
# }