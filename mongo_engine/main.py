import timeit

import redis
from redis_lru import RedisLRU

from models import Authors, Quotes
import connect

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def parser_command(commands_):
    return commands_.strip().split(":")


def handler_command(command_, data_):
    match command_:
        case "name":
            start = timeit.default_timer()
            print(find_author(data_.strip()))
            print(f"Spend time: {timeit.default_timer()-start}")
        case "tag":
            start = timeit.default_timer()
            print(find_tag(data_.strip()))
            print(f"Spend time: {timeit.default_timer() - start}")
        case "tags":
            start = timeit.default_timer()
            find_tags(data_.strip())
            print(f"Spend time: {timeit.default_timer() - start}")
        case _:
            print("I don't know what you mean. Try again.")


@cache
def find_author(data_):
    authors = Authors.objects(fullname__icontains=data_)
    if authors:
        result = ""
        for author in authors:
            result += f"{author.fullname}:\n"
            for q in Quotes.objects.filter(author=author):
                result += f"{q.quote}\n"
        return result[:-2]
    else:
        return f"{data_} not found"


@cache
def find_tag(data_):
    values_ = Quotes.objects(tags__icontains=data_)
    if values_:
        result = ""
        for tag in values_:
            tags = []
            for _ in tag.tags:
                if data_ in _:
                    tags.append(_)
            result += f"tag: {tags}:  {tag.quote}\n"
        return result[:-2]
    else:
        return f"{data_} not found"


def find_tags(data_):
    values_ = data_.strip().split(",")
    for value in values_:
        print(f"Quotes for tag '{value}':")
        print(find_tag(value.strip()))


if __name__ == '__main__':
    while True:
        commands = input("Enter the command: ")
        if commands == "exit":
            print("Bye!")
            break
        else:
            try:
                command, data = parser_command(commands)
                handler_command(command, data)
            except ValueError as err:
                print(err)
