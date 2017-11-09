import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, args):
        return 'Hello from GraphQL!'

schema = graphene.Schema(query=Query)
