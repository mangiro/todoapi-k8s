from enum import Enum
from typing import Optional

from pydantic import BaseModel


def to_camel(key):
    splitted = key.split("_")
    return "".join(
        word.title() if splitted.index(word) else word for word in splitted
    )


class TaskStatusEnum(str, Enum):
    done = "DONE"
    pending = "PENDING"
    in_progress = "IN_PROGRESS"


class TaskBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatusEnum]


class TaskCreate(BaseModel):
    name: str
    description: str


class TaskUpdate(TaskBase):
    ...


class TaskInDBBase(TaskBase):
    id: int

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class TaskObj(TaskInDBBase):
    ...
