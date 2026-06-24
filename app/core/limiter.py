import asyncio


class DatabaseLimiter:
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)


db_limiter: DatabaseLimiter | None = None


def get_db_limiter() -> DatabaseLimiter:
    global db_limiter
    if db_limiter is None:
        raise RuntimeError("DatabaseLimiter not initialized. Call init_db_limiter() first.")
    return db_limiter


def init_db_limiter(max_concurrent: int) -> DatabaseLimiter:
    global db_limiter
    if db_limiter is None:
        db_limiter = DatabaseLimiter(max_concurrent)
    return db_limiter
