from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class PaginationMetadata(BaseModel):
    totalItems: int
    itemCount: int
    itemsPerPage: int
    totalPages: int
    currentPage: int
    hasMore: bool


class PowerResponsePaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    pagination: PaginationMetadata

    class Config:
        arbitrary_types_allowed = True
