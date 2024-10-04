from typing import Generic, List, Type, TypeVar

T = TypeVar('T')


class PaginationMetadata():
    totalItems: int
    itemCount: int
    itemsPerPage: int
    totalPages: int
    currentPage: int
    hasMore: bool

    def __init__(self, data):
        self.totalItems = data.get('totalItems')
        self.itemCount = data.get('itemCount')
        self.itemsPerPage = data.get('itemsPerPage')
        self.totalPages = data.get('totalPages')
        self.currentPage = data.get('currentPage')
        self.hasMore = data.get('hasMore')


class PowerResponsePaginatedResponse(Generic[T]):
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

    def generic_class_type(self) -> Type[T]:
        return self.__class__.__orig_bases__[0].__args__[0]

    def __init__(self, item_class: Type[T], items: List[T], pagination: PaginationMetadata):
        self.items = [item_class(item) for item in items]
        self.pagination = PaginationMetadata(pagination)
