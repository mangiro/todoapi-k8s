from typing import Dict, Any

from sqlalchemy import Text, Integer, String, Column
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from .db import metadata


class_registry: Dict = {}


@as_declarative(class_registry=class_registry, metadata=metadata)
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=True)
    description = Column(Text(500), nullable=True)
    status = Column(String, nullable=True, default="PENDING")
