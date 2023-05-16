from datetime import datetime, timedelta
from typing import TypeVar, Generic

T = TypeVar("T")


class CacheExpiredError(Exception):
    def __init__(self, value, last_update: datetime):
        self.value = value
        self.last_update: datetime = last_update


class MemoryCached(Generic[T]):
    def __init__(self, value: T, ttl: timedelta):
        self.value: T = value
        self.ttl: timedelta = ttl
        self.default_ttl: timedelta = ttl
        self.last_update: datetime = datetime.now()

    def set(self, value: T, ttl: timedelta | None = None):
        if ttl is None:
            self.ttl = self.default_ttl
        else:
            self.ttl = ttl

        self.value = value
        self.last_update = datetime.now()

    def get(self) -> T:
        if self.last_update - datetime.now() >= self.ttl:
            raise CacheExpiredError(self.value, self.last_update)

        return self.value
