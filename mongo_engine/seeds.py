import json

import connect

from datetime import datetime
from models import Authors, Quotes

import pathlib

author_file = pathlib.Path(__file__).parent.parent.joinpath("authors.json")
quotes_file = pathlib.Path(__file__).parent.parent.joinpath("quotes.json")

with open(author_file, "r", encoding="utf-8") as fd:
    authors = json.load(fd)

for data in authors:
    author = Authors(
        fullname=data.get("fullname"),
        born_location=data.get("born_location"),
        description=data.get("description"),
        born_date=datetime.strptime(data.get("born_date"), "%B %d, %Y").date(),
    )
    author.save()

with open(quotes_file, "r", encoding="utf-8") as fd:
    quotes = json.load(fd)
for data in quotes:
    quote = Quotes()
    quote.tags = data.get("tags")
    quote.quote = data.get("quote")
    author = Authors.objects.filter(fullname=data.get("author")).first()
    if author:
        quote.author = author
    quote.save()
