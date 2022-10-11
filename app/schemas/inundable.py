from marshmallow import Schema, fields


class InundableSchema(Schema):
    id = fields.Int()
    code = fields.Str()
    name = fields.Str()
    coordinates = fields.Str()
    status = fields.Str()
    color = fields.Str()


class InundablePaginationSchema(Schema):
    # page = fields.Int()
    # per_page = fields.Int()
    # page = fields.String()
    # total = fields.String()
    total = fields.String(attribute="total")
    pagina = fields.String(attribute="page")
    items = fields.Nested(InundableSchema, many=True, data_key="inundables")


inundables_schema = InundableSchema(many=True)
inundable_schema = InundableSchema()
inundable_pagination_schema = InundablePaginationSchema()
# Si no quiero que funcione para una coleccion
