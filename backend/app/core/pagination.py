def paginate(items: list, limit: int = 100, offset: int = 0) -> list:
    return items[offset: offset + limit]
