from marshmallow import Schema, fields


class LocationSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    address = fields.Str()
    status = fields.Int()
    telephone = fields.Str()
    email = fields.Email()
    coordinates = fields.Str()
    latitude = fields.Str()
    longitude = fields.Str()

class LocationPaginationSchema(Schema):
    total = fields.String(attribute="total")
    pagina = fields.String(attribute="page")
    items = fields.Nested(LocationSchema, many=True, data_key="locations")

locations_schema = LocationSchema()
location_pagination_schema = LocationPaginationSchema()
# Si no quiero que funcione para una coleccion
