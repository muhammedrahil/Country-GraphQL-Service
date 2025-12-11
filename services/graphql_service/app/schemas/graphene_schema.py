import graphene


data = [
    {"name": "Hello"},
    {"name": "Hello"},
    {"name": "Hello"},
    {"name": "Hello"},
    {"name": "Hello"},
]


class Person(graphene.ObjectType):
    name = graphene.String()


class DemoQuery(graphene.ObjectType):
    persons = graphene.List(Person)

    def resolve_persons(self, info):
        return [Person(name=item["name"]) for item in data]


graphene_schema = graphene.Schema(query=DemoQuery)
