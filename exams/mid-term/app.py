from flask import Flask, jsonify, request
from marshmallow import ValidationError

from model import *

app = Flask(__name__)

users = {}
ids = {"tweets_id": 0, "users_id": 0}


@app.route('/users', methods=['POST'], endpoint='create')
def create():
    content = request.json
    req_model = UserReq()
    try:
        result = req_model.load(content)
        ids["users_id"] += 1
        response = UserRes(str(ids["users_id"]), result["name"], str(result["email"]).lower(), [], [])
        users[response.id] = response
    except ValidationError as err:
        return jsonify(err.messages), 400
    return response.to_json(), 200


@app.route('/users/<user_id>', methods=['GET'], endpoint='get')
def get(user_id: str):
    if user_id in users:
        value: UserRes = users[user_id]
        return value.to_json(), 200
    else:
        return {"error": "User not found"}, 400


@app.route('/users/<user_id>/timeline', methods=['GET'], endpoint='get_timeline')
def get_timeline(user_id: str):
    if user_id in users:
        value: UserRes = users[user_id]
        followers = value.get_followers()
        tweets = value.get_tweets()
        timeline = []
        for t in tweets:
            timeline.append(Timeline(user_id, t.id, t.tweet))
        for i in followers:
            if i != user_id:
                t: UserRes = users[i]
                tweets = t.get_tweets()
                for t in tweets:
                    timeline.append(Timeline(i, t.id, t.tweet))
        timeline = sorted(timeline, key=lambda x: int(x.tweet_id), reverse=False)
        return TimelineRes(timeline).to_json(), 200
    else:
        return {"error": "User not found"}, 400


@app.route('/users/<user_id>/followers/<follower_id>', methods=['PATCH'], endpoint='add_follower')
def add_follower(user_id: str, follower_id: str):
    if user_id and follower_id is not None and not "":
        if user_id in users:
            if follower_id in users:
                value: UserRes = users[user_id]
                followers = value.get_followers()
                followers.append(follower_id)
                value.set_followers(followers)
                return value.to_json(), 200
            else:
                return {"error": "Follower not found"}, 400
        else:
            return {"error": "User not found"}, 400
    return {"error": "User id and follower id cannot be empty"}, 400


@app.route('/users/<user_id>/tweets', methods=['POST'], endpoint='tweet')
def tweet(user_id: str):
    if user_id is not None and not "":
        content = request.json
        req_model = TweetReq()
        try:
            result = req_model.load(content)
            if user_id not in users:
                return {"error": "User not found"}, 400
            value: UserRes = users[user_id]
            ids["tweets_id"] += 1
            user_tweet = TweetRes(str(ids["tweets_id"]), result["tweet"])
            tweets = value.get_tweets()
            tweets.append(user_tweet)
            value.set_tweets(tweets)
            return user_tweet.to_json(), 200
        except ValidationError as err:
            return jsonify(err.messages), 400
    return {"error": "User id cannot be empty"}, 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
