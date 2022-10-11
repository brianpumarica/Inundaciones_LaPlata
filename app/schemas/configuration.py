from marshmallow import Schema, fields

class ConfigurationSchema(Schema):
    order = fields.Int()
    per_page = fields.Str()
    color_public = fields.Str()
    color_private = fields.Str()


configuration_schema = ConfigurationSchema()