from asyncio import wait
import re
from app.model.item_in_warehouse import ItemInWarehouse
from app.model.view.item_in_warehouse_view import ItemInWarehouseView
from app.redis_client import redis_client
from app.model.item import Item
from app.model.seller import Seller
from app.model.view.item_view import ItemView
from app.model.view.seller_view import SellerView
from app.model.view.warehouse_view import WarehouseView
from app.model.warehouse import Warehouse


class ModelMapper():
    def map(self, entity):
        if isinstance(entity, Item):
            return ItemView(id=entity.id, name=entity.name, price=entity.price, in_stock=entity.in_stock)
        elif isinstance(entity, ItemView):
            return Item(id=entity.id, name=entity.name, price=entity.price, in_stock=bool(entity.in_stock))
        elif isinstance(entity, Seller):
            return SellerView(id=entity.id, name=entity.name)
        elif isinstance(entity, SellerView):
            return Seller(id=entity.id, name=entity.name)
        elif isinstance(entity, Warehouse):
            return WarehouseView(id=entity.id, name=entity.name, address=entity.address, seller_id=entity.seller.id)
        elif isinstance(entity, WarehouseView):
            redis = redis_client.get_client()
            seller = await redis.hgetall(f"seller:{entity.seller_id}")
            if not seller:
                raise Exception("Seller not found")
            seller = Seller(**seller)
            return Warehouse(id=entity.id, name=entity.name, address=entity.address, seller=seller)
        elif isinstance(entity, ItemInWarehouse):
            return ItemInWarehouseView(item_id=entity.item.id, warehouse_id=entity.warehouse.id, quantity=entity.quantity)
        elif isinstance(entity, ItemInWarehouseView):
            redis = redis_client.get_client()
            item = await redis.hgetall(f"item:{entity.item_id}")
            warehouse = await redis.hgetall(f"item:{entity.warehouse_id}")
            if not item or not warehouse:
                raise Exception("Item or Warehouse not found")
            item = Item(**item)
            warehouse = Warehouse(**warehouse)
            return ItemInWarehouse(item=item, warehouse=warehouse, quantity=entity.quantity)
