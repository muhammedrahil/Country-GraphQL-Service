import graphene


class AddCountryInput(graphene.InputObjectType):
    """Input type for adding a new country."""

    name = graphene.String(required=True)
    alpha2_code = graphene.String(required=True)
    alpha3_code = graphene.String(required=True)
    capital = graphene.String()
    region = graphene.String()
    subregion = graphene.String()
    population = graphene.Int()
    area = graphene.Float()
    latitude = graphene.Float()
    longitude = graphene.Float()
    calling_codes = graphene.List(graphene.String)
    timezones = graphene.List(graphene.String)
    currencies = graphene.List(graphene.String)
    languages = graphene.List(graphene.String)
    flag_svg = graphene.String()
    flag_png = graphene.String()
    independent = graphene.Boolean()
