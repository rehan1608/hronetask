from pydantic import BaseModel
from typing import List, Any, Optional

class Page(BaseModel):
    next: Optional[str] = None
    limit: int
    previous: Optional[str] = None

class PaginatedResponse(BaseModel):
    data: List[Any] # Can be a list of products or orders
    page: Page