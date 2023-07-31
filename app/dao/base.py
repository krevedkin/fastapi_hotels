from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            session: AsyncSession
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            session: AsyncSession
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            session: AsyncSession
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def insert_record(cls, **data):
        async with async_session_maker() as session:
            session: AsyncSession
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete_record(cls, **filter_by):
        async with async_session_maker() as session:
            session: AsyncSession
            stmt = delete(cls.model).filter_by(**filter_by)
            await session.execute(stmt)
            await session.commit()
