from marshmallow import Schema, fields


class RouteSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    coordinates = fields.Str()
    status = fields.Email()

class RoutePaginationSchema(Schema):
    total = fields.String(attribute="total")
    pagina = fields.String(attribute="page")
    items = fields.Nested(RouteSchema, many=True, data_key="recorridos")

routes_schema = RouteSchema()
route_pagination_schema = RoutePaginationSchema()
# Si no quiero que funcione para una coleccion
