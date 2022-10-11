from marshmallow import Schema, fields


class ComplaintSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    date_creation = fields.DateTime()
    date_closed = fields.DateTime()
    status = fields.Str()
    surname_user = fields.Str()
    name_user = fields.Str()
    telephone = fields.Str()
    email = fields.Email()
    coordinates = fields.Str()
    from_user = fields.Int()
    category = fields.Int()
    count_calls = fields.Int()
    coordinates = fields.Str()

class ComplaintPaginationSchema(Schema):
    total = fields.String(attribute="total")
    pagina = fields.String(attribute="page")
    items = fields.Nested(ComplaintSchema, many=True, data_key="complaints")


complaints_schema = ComplaintSchema(many=True)
complaint_schema = ComplaintSchema()
complaint_pagination_schema = ComplaintPaginationSchema()
# Si no quiero que funcione para una coleccion
