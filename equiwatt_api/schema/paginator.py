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
    """
    PowerResponsePaginatedResponse represents a paginated response from equiwatt PowerResponse that contains
    a list of items and pagination metadata.
    Attributes:
    ----------
    items : List[T]
        A list of items of generic type `T`.
    pagination : PaginationMetadata
        Metadata for pagination, containing details such as current page, total pages, etc.
    """
    items: List[T]
    pagination: PaginationMetadata

    class Config:
        arbitrary_types_allowed = True
