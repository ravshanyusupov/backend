from asgiref.sync import sync_to_async


@sync_to_async
def paginate_response(queryset, Schema, page: int = 1, size: int = 10, ordering: list = ["-id"]):
    offset = (page - 1) * size
    limit = size

    items = [
        Schema.from_orm(item).dict()
        for item in queryset.order_by(*ordering)[offset : offset + limit]
    ]
    total = queryset.count()

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
    }


def get_max_pages(total_items, size):
    if size <= 0:
        return 1
    return (total_items + size - 1) // size
