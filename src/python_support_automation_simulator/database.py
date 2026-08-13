from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


def create_engine_for_url(database_url: str) -> Engine:
    options: dict[str, object] = {"future": True, "connect_args": {"check_same_thread": False}}
    if ":memory:" in database_url:
        options["poolclass"] = StaticPool
    return create_engine(database_url, **options)


def create_session_factory(database_url: str):
    return sessionmaker(bind=create_engine_for_url(database_url), autoflush=False, expire_on_commit=False)
