#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库优化脚本
为book.db添加索引，优化查询性能
"""

import sqlite3
import sys
import os

# 索引定义
INDEXES = [
    # 分类索引 - 加速按分类浏览
    ("idx_book_categories", "CREATE INDEX IF NOT EXISTS idx_book_categories ON book(categories)"),

    # 作者索引 - 加速按作者查询
    ("idx_book_author", "CREATE INDEX IF NOT EXISTS idx_book_author ON book(author)"),

    # 更新时间索引 - 加速按更新时间排序
    ("idx_book_updated", "CREATE INDEX IF NOT EXISTS idx_book_updated_at ON book(updated_at DESC)"),

    # 点赞数索引 - 加速按热度排序
    ("idx_book_likes", "CREATE INDEX IF NOT EXISTS idx_book_likesCount ON book(likesCount DESC)"),

    # 创建时间索引
    ("idx_book_created", "CREATE INDEX IF NOT EXISTS idx_book_created_at ON book(created_at DESC)"),

    # 复合索引 - 优化常见的多条件查询
    ("idx_book_category_likes", "CREATE INDEX IF NOT EXISTS idx_book_category_likes ON book(categories, likesCount DESC)"),

    # 完结状态索引
    ("idx_book_finished", "CREATE INDEX IF NOT EXISTS idx_book_finished ON book(finished)"),

    # 标题索引（用于搜索）
    ("idx_book_title", "CREATE INDEX IF NOT EXISTS idx_book_title ON book(title)"),
]

# 性能优化配置
PRAGMA_SETTINGS = [
    "PRAGMA journal_mode=WAL",        # Write-Ahead Logging，提升并发性能
    "PRAGMA synchronous=NORMAL",      # 平衡性能和安全性
    "PRAGMA cache_size=-64000",       # 64MB缓存
    "PRAGMA temp_store=MEMORY",       # 临时表存储在内存
    "PRAGMA mmap_size=268435456",     # 256MB内存映射
]


def get_db_path():
    """获取数据库路径"""
    # 默认路径
    db_paths = [
        "db/book.db",
        "../src/db/book.db",
        "src/db/book.db",
    ]

    # 尝试找到数据库文件
    for path in db_paths:
        if os.path.exists(path):
            return path

    # 如果没找到，返回默认路径
    return "db/book.db"


def optimize_database(db_path):
    """优化数据库"""
    print(f"=== 数据库优化工具 ===")
    print(f"数据库路径: {db_path}")

    if not os.path.exists(db_path):
        print(f"错误: 数据库文件不存在: {db_path}")
        return False

    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. 应用PRAGMA设置
        print("\n[1/4] 应用性能优化配置...")
        for pragma in PRAGMA_SETTINGS:
            print(f"  执行: {pragma}")
            cursor.execute(pragma)

        # 2. 检查现有索引
        print("\n[2/4] 检查现有索引...")
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND sql IS NOT NULL")
        existing_indexes = {row[0]: row[1] for row in cursor.fetchall()}
        print(f"  现有索引数量: {len(existing_indexes)}")

        # 3. 创建新索引
        print("\n[3/4] 创建优化索引...")
        created = 0
        skipped = 0

        for idx_name, idx_sql in INDEXES:
            if idx_name in existing_indexes:
                print(f"  ⊙ 跳过已存在: {idx_name}")
                skipped += 1
            else:
                print(f"  ✓ 创建索引: {idx_name}")
                cursor.execute(idx_sql)
                created += 1

        # 4. 优化数据库
        print("\n[4/4] 优化数据库...")

        # ANALYZE - 更新查询优化器统计信息
        print("  执行: ANALYZE")
        cursor.execute("ANALYZE")

        # 获取数据库统计信息
        cursor.execute("SELECT COUNT(*) FROM book")
        book_count = cursor.fetchone()[0]

        cursor.execute("PRAGMA page_count")
        page_count = cursor.fetchone()[0]

        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]

        db_size_mb = (page_count * page_size) / (1024 * 1024)

        # 提交更改
        conn.commit()
        conn.close()

        # 输出统计
        print("\n=== 优化完成 ===")
        print(f"数据库大小: {db_size_mb:.2f} MB")
        print(f"书籍数量: {book_count:,}")
        print(f"总索引数: {len(existing_indexes) + created}")
        print(f"  - 已存在: {skipped}")
        print(f"  - 新创建: {created}")

        if created > 0:
            print("\n✓ 成功创建 {} 个索引，查询性能预计提升 3-10 倍".format(created))
        else:
            print("\n✓ 数据库已是最优状态")

        return True

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_indexes(db_path):
    """验证索引"""
    print("\n=== 验证索引 ===")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND sql IS NOT NULL")
        indexes = [row[0] for row in cursor.fetchall()]

        print(f"数据库中的索引 ({len(indexes)}个):")
        for idx in sorted(indexes):
            print(f"  - {idx}")

        conn.close()
        return True

    except Exception as e:
        print(f"错误: {e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = get_db_path()

    # 优化数据库
    success = optimize_database(db_path)

    if success:
        # 验证索引
        verify_indexes(db_path)
        print("\n提示: 重启应用后优化将生效")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
