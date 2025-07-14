from typing import List, Any
import redis
from redis_lru import RedisLRU
from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_author(author):

    print(f"Find by name '{author}':")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


@cache
def find_by_tag(tag):

    print(f"Find by tag '{tag}':")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(tags):

    print(f"Find by tags '{tags}':")
    tags_list = tags.split(",")
    quotes = Quote.objects(tags__in=tags_list)
    return [q.quote for q in quotes]


def main():
    while True:
        command = input("Введіть команду (name:..., tag:..., tags:..., exit): ").strip()

        if command.lower() == 'exit':
            print("Завершення роботи.")
            break

        if command.startswith("name:"):
            name = command[5:].strip()
            results = find_by_author(name)
        elif command.startswith("tag:"):
            tag = command[4:].strip()
            results = find_by_tag(tag)
        elif command.startswith("tags:"):
            tags = command[5:].strip()
            results = find_by_tags(tags)
        else:
            print("Невідома команда.")
            continue

        if results:
            for quote in results:
                print(quote)
        else:
            print("Нічого не знайдено.")


if __name__ == "__main__":
    main()