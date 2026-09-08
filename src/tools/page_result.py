from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

from tools.pagination import SEARCH_PAGE_SIZE, clamp_page, page_count


T = TypeVar("T")


@dataclass(frozen=True)
class PageRequest:
    page: int = 1
    page_size: int = SEARCH_PAGE_SIZE

    def __post_init__(self):
        if self.page < 1 or self.page_size < 1:
            raise ValueError("页号和每页数量必须大于零")

    @property
    def offset(self):
        return (self.page - 1) * self.page_size

    def clamp(self, total):
        return PageRequest(clamp_page(self.page, page_count(total, self.page_size)), self.page_size)


@dataclass
class PageResult(Generic[T]):
    items: List[T]
    page: int
    pages: int
    total: Optional[int] = None
    page_size: Optional[int] = None

    @classmethod
    def from_total(cls, items, request, total):
        request = request.clamp(total)
        return cls(items, request.page, page_count(total, request.page_size), total, request.page_size)

    @classmethod
    def from_remote(cls, data):
        """远端总页数以接口返回值为准，不套用本地每页数量。"""
        pages = max(1, int(data.get("pages", 1)))
        page = clamp_page(int(data.get("page", 1)), pages)
        total = data.get("total")
        page_size = data.get("limit")
        return cls(data.get("docs", []), page, pages, int(total) if total is not None else None,
                   int(page_size) if page_size is not None else None)
