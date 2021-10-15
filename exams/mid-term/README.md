# Coding Question

You will be implementing Twitter-like REST API to support the following features. Please name main Flask file [app = Flask(__name__)] as app.py. 

- You can use any Flask plugin or other Python modules to implement the solution.
- Your implementation does NOT require to persist data into any database. You can simply store all data in a Python dictionary.

## APIs

* POST /users (Create new user)

_Request_

```json
{
    "name": "John Smith",
    "email": "john.smith@gmail.com"
}
```

_Response_

200

```json
{
    "id": "100",
    "name": "John Smith",
    "email": "john.smith@gmail.com",
    "tweets": [],
    "followers": []
}
```

* PATCH /users/{user_id}/followers/{follower_id} (Create new follower)

### Follower is an alias to user and you do not need to create Follower model. Follower id is an user id.

_Request_

Example: PATCH /users/{100}/followers/{101}

_Response_

200

```json
{
    "id": "100",
    "name": "John Smith",
    "email": "john.smith@gmail.com",
    "tweets": [],
    "followers": [ "101" ]
}
```

* POST /users/{user_id}/tweets

_Request_

```json
{
    "tweet": "Fan art is the best"
}
```

_Response_

200

```json
{ 
    "tweet_id" : "1", 
    "tweet": "Fan art is the best"
}
```

* GET /users/{user_id} (Get user details, a list of tweets, and a list of followers.)

_Response_

200

```json
{
    "id": "100",
    "name": "John Smith",
    "email": "john.smith@gmail.com",
    "tweets": [ { "tweet_id" : "1", "tweet": "Fan art is the best" } ],
    "followers": [ "101" ]
}
```

* GET /users/{user_id}/timeline (Get all tweets from the given user id as well as the followers ordered by 'tweet_id')

_Response_

200

```json
{
    "timeline": [ 
        { "user_id": "100", "tweet_id" : "1", "tweet": "Fan art is the best" },
        { "user_id": "101", "tweet_id" : "2", "tweet": "Vaccines have a proven track record of saving lives. Let’s keep it going!" },
        { "user_id": "101", "tweet_id" : "3", "tweet": "Hello Everyone" }
    ]
}
```