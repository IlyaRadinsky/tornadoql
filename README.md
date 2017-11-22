A [Tornado](http://www.tornadoweb.org/) boilerplate for [Graphene](http://graphene-python.org/) with subscriptions.

Forked from Ilya Radinsky's example for a Tornado Web Server Integration with Graphene and packaged into a generalized, simple package for creating GraphQL API servers that support Websockets, using two imports and one line of code.

While the default way to expose a graphene schema as a GraphQL API is one line of code, the package is setup so that you can also make that API part of a larger application by simply adding to the GraphQL endpoints before calling start. Getting your own API only server up is as simple as:

```python
from tornadoql.tornadoql import TornadoQL
from my_schema import my_schema

TornadoQL.start(my_schema)

```

This will start a server with /graphql, /graphiql, and /subscriptions endpoints, using optoinal arguments for . The version of graphiql included in the original fork is enhanced to support queries on subscriptions.

