from redis.asyncio.retry import Retry
from app.model.item import Item
from app.model.view.item_view import ItemView


class ModelMapper():
    def map(self, entity):
        if isinstance(entity, Item):
            return ItemView(id=entity.id, name=entity.name, price=entity.price, in_stock=entity.in_stock)
        elif isinstance(entity, ItemView):
            return Item(id=entity.id, name=entity.name, price=entity.price, in_stock=bool(entity.in_stock))
