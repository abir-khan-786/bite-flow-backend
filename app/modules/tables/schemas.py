from pydantic import BaseModel
from prisma.enums import TableStatus

class TableCreateSchema(BaseModel):
    tableNumber: str
    capacity: int = 4

class TableStatusUpdateSchema(BaseModel):
    status: TableStatus