from pydantic import BaseModel

class InventoryCreateSchema(BaseModel):
    itemName: str
    quantity: float
    unit: str
    minThreshold: float = 10.0

class InventoryUpdateStockSchema(BaseModel):
    quantity: float