import graphene

data = [
    {"name": "Hello", "email": "fcdd"},
    {"name": "Hello", "email": "fcdd"},
    {"name": "Hello", "email": "fcdd"},
    {"name": "Hello", "email": "fcdd"},
    {
        "name": "Hello",
    },
]


class Person(graphene.ObjectType):
    name = graphene.String()
    email = graphene.String()


class DemoQuery(graphene.ObjectType):
    persons = graphene.List(Person)

    def resolve_persons(self, info):
        return data


graphene_schema = graphene.Schema(query=DemoQuery)
