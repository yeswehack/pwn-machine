#!/usr/bin/env python
from graphene import ObjectType, String, Schema, Field, ID
from flask import Flask
from flask_graphql import GraphQLView
""" from docker import client


d = client.from_env()
print(d) """
app = Flask(__name__)


class ObjectTypeNoExtra(ObjectType):
    pass


class Image(ObjectType):
    id = ID()
    name = String(default_value="toto")


class Container(ObjectType):
    id = ID()
    image: Image()
    name: String()


class Query(ObjectType):
    image = Field(Image, name=String())
    container = Field(Container, id=String())

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_image(root, info, name):
        info = {"id": "toto", "name": name, "pouet": 42}
        return Image(**info)

    def resolve_container(root, info):
        return "See ya!"


schema = Schema(query=Query)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
    ),
)

# Optional, for adding batch query support (used in Apollo-Client)
# app.add_url_rule(
#    "/graphql/batch",
#    view_func=GraphQLView.as_view("graphql", schema=schema, batch=True),
# )

if __name__ == "__main__":
    app.run(port=4000, debug=True)
