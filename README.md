A [Tornado](http://www.tornadoweb.org/) boilerplate for [Graphene](http://graphene-python.org/) with subscriptions.

Forked from Ilya Radinsky's example for a Tornado Web Server Integration with Graphene and packaged into a generalized, simple package for creating GraphQL API servers that support Websockets with just a few lines of code.

While the default way to expose a graphene schema as a GraphQL API is only a few lines. The package is setup so that you could also make that API part of a larger application with more endpoints. Getting started with an API only server is as simple as:

```python
from tornadoql.tornadoql import TornadoQL
from my_schema import my_schema

TornadoQL.start(my_schema)

```

This will start a server with /graphql, /graphiql, and /subscriptions endpoints. The version of graphiql included in the original fork is enhanced to support queries on subscriptions.

