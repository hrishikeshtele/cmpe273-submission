import json

from marshmallow import Schema, fields


class UserReq(Schema):
    id = fields.String(required=False)
    name = fields.String(required=True)
    email = fields.Email(required=True)


class TweetReq(Schema):
    tweet = fields.String(required=True)


class TweetRes:
    tweet_id = fields.String(required=True)
    tweet = fields.String(required=True)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, id: str, tweet: str) -> None:
        self.id = id
        self.tweet = tweet


class Timeline:
    user_id: str
    tweet_id: str
    tweet: str

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, user_id: str, tweet_id: str, tweet: str) -> None:
        self.user_id = user_id
        self.tweet_id = tweet_id
        self.tweet = tweet


class TimelineRes:
    timeline: [Timeline]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, timeline: [Timeline]) -> None:
        self.timeline = timeline


class UserRes:
    id: str
    name: str
    email: str
    tweets: [TweetRes]
    followers: [str]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, id: str, name: str, email: str, tweets: [TweetRes], followers: [str]) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.tweets = tweets
        self.followers = followers

    def set_followers(self, followers):
        self.followers = followers

    def get_followers(self):
        return self.followers

    def set_tweets(self, tweets):
        self.tweets = tweets

    def get_tweets(self):
        return self.tweets
