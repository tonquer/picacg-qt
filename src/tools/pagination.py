SEARCH_PAGE_SIZE = 20
FAVORITE_PAGE_SIZE = 100
HISTORY_PAGE_SIZE = 20
LOCAL_BOOK_PAGE_SIZE = 30


def page_count(total, page_size):
    """空列表保留第一页，整页数量不多算一页。"""
    return max(1, (max(0, total) + page_size - 1) // page_size)


def clamp_page(page, pages):
    return min(max(1, page), max(1, pages))
