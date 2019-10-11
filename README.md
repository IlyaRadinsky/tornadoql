A [Tornado](http://www.tornadoweb.org/) boilerplate for [Graphene](http://graphene-python.org/) with subscriptions.

Installation
------------
```sh
git clone https://github.com/IlyaRadinsky/tornadoql
cd tornadoql
python3 setup.py install
```

Using
-----
A very easy to use, fully extensible Tornado Web Server Integration with Graphene to make serving GraphQL APIs, including Websocket subscriptions, as easy as defining your schema.

With TornadoQL, exposing a graphene schema as a GraphQL API takes two imports and one line of code. You can also make that API part of a larger application by simply adding to the GraphQL endpoints and Tornado application settings before calling start. Getting your own API-only server up is as simple as defining a Graphene schema and the following code:

```python
import graphene
from tornadoql.tornadoql import TornadoQL

class TestType(graphene.ObjectType):
    id = graphene.ID()
    value = graphene.String()

class Query(graphene.ObjectType):
    test = graphene.Field(TestType)

    def resolve_test(self, info):
        return TestType(id='1', value='test value')

schema = graphene.Schema(query=Query)

TornadoQL.start(schema)

```

This will start a server with `/graphql`, `/graphiql`, and `/subscriptions` endpoints, supporting optional arguments for port and application settings. TornadoQL includes an extended version of graphiql GraphQL browser that supports subscriptions as well as queries and mutations.

```
Starting GraphQL server on 8888

  GraphiQL:              http://localhost:8888/graphiql
  Queries and Mutations: http://localhost:8888/graphql
  Subscriptions:         ws://localhost:8888/subscriptions
  
```
