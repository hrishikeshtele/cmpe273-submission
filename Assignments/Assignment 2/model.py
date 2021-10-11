import json

from marshmallow import Schema, fields


class ShortenReq(Schema):
    long_url = fields.String(required=True)
    domain = fields.String(required=False)


class ShortenRes:
    link: str
    id: str
    long_url: str
    created_at: str

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, link: str, id: str, long_url: str, created_at: str) -> None:
        self.link = link
        self.id = id
        self.long_url = long_url
        self.created_at = created_at


class CreateReq(Schema):
    long_url = fields.String(required=True)
    domain = fields.String(required=False)
    title = fields.String(required=False)
    tags = fields.List(fields.String)


class CreateRes:
    id: str
    link: str
    long_url: str
    created_at: str
    title: str
    tags: [str]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, link: str, id: str, long_url: str, created_at: str, title: str, tags: [str]) -> None:
        self.id = id
        self.link = link
        self.long_url = long_url
        self.created_at = created_at
        self.title = title
        self.tags = tags


class UpdateReq(Schema):
    long_url = fields.String(required=False)
    title = fields.String(required=False)
    tags =  fields.List(fields.String)


class UpdateRes:
    id: str
    link: str
    long_url: str
    created_at: str
    title: str
    tags: [str]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, link: str, id: str, long_url: str, created_at: str, title: str, tags: [str]) -> None:
        self.id = id
        self.link = link
        self.long_url = long_url
        self.created_at = created_at
        self.title = title
        self.tags = tags


class UrlData:
    link: str
    id: str
    long_url: str
    created_at: str
    title: str
    tags: [str]
    hits: int

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, link: str, id: str, long_url: str, created_at: str, title: str, tags: [str], hits: int) -> None:
        self.link = link
        self.id = id
        self.long_url = long_url
        self.created_at = created_at
        self.title = title
        self.tags = tags
        self.hits = hits


class ClickRes:
    total_clicks: str
    link: str
    long_url: str
    created_at: str

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__(self, link: str, total_clicks: str, long_url: str, created_at: str) -> None:
        self.link = link
        self.total_clicks = total_clicks
        self.long_url = long_url
        self.created_at = created_at
