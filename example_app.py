"""
TornadoQL server as a simple example or skeleton
"""
from tornadoql.tornadoql import TornadoQL, PORT
from example_schema import DEFAULT_SCHEMA

def main():
    print('GraphQL server starting on %s' % PORT)
    TornadoQL.start(DEFAULT_SCHEMA)

if __name__ == '__main__':
    main()
