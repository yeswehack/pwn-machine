#!/usr/bin/env python

from graphene import Schema
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
import schemas
from schemas.utils import get_mutations, get_queries, get_subscriptions
import time


app = Flask(__name__)
CORS(app)

slow = 0

@app.before_request
def sleep():
    if slow:
        time.sleep(slow)


schema = Schema(query=get_queries(), mutation=get_mutations(), subscription=get_subscriptions())
with open("schema.gql", "w") as f:
    f.write(str(schema))


app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
    ),
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
