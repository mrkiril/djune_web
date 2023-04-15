import uuid
from datetime import datetime
from typing import Any, NewType
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from settings import config

metadata = sa.MetaData()


DeclarativeBase: Any = declarative_base(metadata=metadata)

sessionmaker = async_sessionmaker[AsyncSession]


def get_db_url(driver: str = "asyncpg") -> str:
    return (
        f"postgresql+{driver}://{config.postgres_user}:{config.postgres_password}"
        f"@{config.postgres_host}:{config.postgres_port}/{config.postgres_db}"
    )


db_engine = create_async_engine(
        get_db_url(),
        connect_args={
            "server_settings": {
                "application_name": "web_jun",
                "statement_timeout": "10000",
            },
        },
        pool_size=5,
    )

db_session = sessionmaker(db_engine, expire_on_commit=False)


class Currency(DeclarativeBase):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(sa.INT(), primary_key=True, autoincrement=True)
    currency_from: Mapped[str] = mapped_column(sa.VARCHAR(32), nullable=False)
    currency_to: Mapped[str] = mapped_column(sa.VARCHAR(32), nullable=False)
    amount: Mapped[float] = mapped_column(sa.FLOAT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, nullable=False)



# async with db_session.begin() as session:
#     user = await session.get(User, user_id)
