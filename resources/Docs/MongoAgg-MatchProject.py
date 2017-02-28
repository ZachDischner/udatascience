#!/usr/bin/env python
"""
Write an aggregation query to answer this question:

Of the users in the "Brasilia" timezone who have tweeted 100 times or more,
who has the largest number of followers?

The following hints will help you solve this problem:
- Time zone is found in the "time_zone" field of the user object in each tweet.
- The number of tweets for each user is found in the "statuses_count" field.
  To access these fields you will need to use dot notation (from Lesson 4)
- Your aggregation query should return something like the following:
{u'ok': 1.0,
 u'result': [{u'_id': ObjectId('52fd2490bac3fa1975477702'),
                  u'followers': 2597,
                  u'screen_name': u'marbles',
                  u'tweets': 12334}]}
Note that you will need to create the fields 'followers', 'screen_name' and 'tweets'.

Please modify only the 'make_pipeline' function so that it creates and returns an aggregation 
pipeline that can be passed to the MongoDB aggregate function. As in our examples in this lesson,
the aggregation pipeline should be a list of one or more dictionary objects. 
Please review the lesson examples if you are unsure of the syntax.

Your code will be run against a MongoDB instance that we have provided. If you want to run this code
locally on your machine, you have to install MongoDB, download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.

Please note that the dataset you are using here is a smaller version of the twitter dataset used 
in examples in this lesson. If you attempt some of the same queries that we looked at in the lesson 
examples, your results will be different.
"""

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$match"   : {"user.time_zone":"Brasilia", "user.statuses_count":{"$gt":100}}},
                {"$project" : {"followers":"$user.followers_count", 
                                "screen_name":"$user.screen_name",
                                "tweets":"$user.statuses_count"}},
                {"$sort"    : {"followers":-1}},
                {"$limit"   : 1}
                ]
    return pipeline

def aggregate(db, pipeline):
    return [doc for doc in db.tweets.aggregate(pipeline)]


if __name__ == '__main__':
    db = get_db('twitter')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    import pprint
    pprint.pprint(result)
    assert len(result) == 1
    assert result[0]["followers"] == 17209



###### Document structure:
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
