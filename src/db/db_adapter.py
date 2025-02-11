import os
from dotenv import load_dotenv
from sqlalchemy import MetaData, event, inspect
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from motor.motor_asyncio import AsyncIOMotorClient

class Model(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            'ix': 'ix_%(column_0_label)s',
            'uq': 'uq_%(table_name)s_%(column_0_name)s',
            'ck': 'ck_%(table_name)s_%(constraint_name)s',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'pk': 'pk_%(table_name)s'
        }
    )

class DBAdapter:
    def __init__(self, db_engine: str = 'sqlite'):
        load_dotenv(dotenv_path='./db.env')

        self.db_engine = db_engine
        if db_engine == 'sqlite':
            self.db_url = os.getenv('ASYNCSQLITE_DB_URL')
            self.engine = create_async_engine(self.db_url, echo=True)
            self.session = async_sessionmaker(self.engine, expire_on_commit=False)
        elif db_engine == 'mongo':
            self.db_url = os.getenv('MONGO_DB_URL')
            self.client = AsyncIOMotorClient(self.db_url)
            self.database_name = os.getenv('MONGO_DB_NAME', 'mydatabase')
            self.database = self.client[self.database_name]
        else:
            raise ValueError(f"Unsupported database engine: {db_engine}")

    async def get_session(self):
        if self.db_engine == 'sqlite':
            return self.session()
        elif self.db_engine == 'mongo':
            return self.database
        else:
            raise ValueError(f"Unsupported database engine: {self.db_engine}")

    async def close(self):
        if self.db_engine == 'sqlite' and self.engine:
            await self.engine.dispose()
        elif self.db_engine == 'mongo' and self.client:
            self.client.close()
        else:
            raise ValueError(f"Unsupported database engine: {self.db_engine}")

    @event.listens_for(Model, "init", propagate=True)
    def init_relationships(self, tgt, arg, kw):
        mapper = inspect(tgt.__class__)
        for arg in mapper.relationships:
            if arg.collection_class is None and arg.uselist:
                continue
            if arg.key not in kw:
                kw.setdefault(arg.key, None if not arg.uselist else arg.collection_class())