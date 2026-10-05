from pydantic import BaseModel
from typing import List, Optional
from prisma.enums import OrderType, OrderStatus, PaymentStatus

class OrderItemSchema(BaseModel):
    menuItemId: str
    quantity: int
    notes: Optional[str] = None

class CreateOrderSchema(BaseModel):
    orderType: OrderType = OrderType.DINE_IN
    tableId: Optional[str] = None
    items: List[OrderItemSchema]

class UpdateOrderStatusSchema(BaseModel):
    status: OrderStatusfrom pydantic import BaseModel
from typing import List, Optional
from prisma.enums import OrderType, OrderStatus, PaymentStatus

class OrderItemSchema(BaseModel):
    menuItemId: str
    quantity: int
    notes: Optional[str] = None

class CreateOrderSchema(BaseModel):
    orderType: OrderType = OrderType.DINE_IN
    tableId: Optional[str] = None
    items: List[OrderItemSchema]

class UpdateOrderStatusSchema(BaseModel):
    status: OrderStatusfrom pydantic import BaseModel
from typing import List, Optional
from prisma.enums import OrderType, OrderStatus, PaymentStatus

class OrderItemSchema(BaseModel):
    menuItemId: str
    quantity: int
    notes: Optional[str] = None

class CreateOrderSchema(BaseModel):
    orderType: OrderType = OrderType.DINE_IN
    tableId: Optional[str] = None
    items: List[OrderItemSchema]

class UpdateOrderStatusSchema(BaseModel):
    status: OrderStatusfrom pydantic import BaseModel
from typing import List, Optional
from prisma.enums import OrderType, OrderStatus, PaymentStatus

class OrderItemSchema(BaseModel):
    menuItemId: str
    quantity: int
    notes: Optional[str] = None

class CreateOrderSchema(BaseModel):
    orderType: OrderType = OrderType.DINE_IN
    tableId: Optional[str] = None
    items: List[OrderItemSchema]

class UpdateOrderStatusSchema(BaseModel):
    status: OrderStatusfrom pydantic import BaseModel
from typing import List, Optional
from prisma.enums import OrderType, OrderStatus, PaymentStatus

class OrderItemSchema(BaseModel):
    menuItemId: str
    quantity: int
    notes: Optional[str] = None

class CreateOrderSchema(BaseModel):
    orderType: OrderType = OrderType.DINE_IN
    tableId: Optional[str] = None
    items: List[OrderItemSchema]

class UpdateOrderStatusSchema(BaseModel):
    status: OrderStatusfrom pydantic import BaseModel
from typing import List, Optional
from prisma.enums import OrderType, OrderStatus, PaymentStatus

class OrderItemSchema(BaseModel):
    menuItemId: str
    quantity: int
    notes: Optional[str] = None

class CreateOrderSchema(BaseModel):
    orderType: OrderType = OrderType.DINE_IN
    tableId: Optional[str] = None
    items: List[OrderItemSchema]

class UpdateOrderStatusSchema(BaseModel):
    status: OrderStatusfrom pydantic import BaseModel
from typing import List, Optional
from prisma.enums import OrderType, OrderStatus, PaymentStatus

class OrderItemSchema(BaseModel):
    menuItemId: str
    quantity: int
    notes: Optional[str] = None

class CreateOrderSchema(BaseModel):
    orderType: OrderType = OrderType.DINE_IN
    tableId: Optional[str] = None
    items: List[OrderItemSchema]

class UpdateOrderStatusSchema(BaseModel):
    status: OrderStatus