from mongoengine import Document, ReferenceField, StringField
from mongoengine.fields import DateField, ListField


class Authors(Document):
    fullname = StringField(max_length=50, required=True)
    born_date = DateField()
    born_location = StringField(max_length=100)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    quote = StringField()
    author = ReferenceField(Authors)
