from sqlalchemy import String, ForeignKey, Table, Column, DateTime, Integer, select
from typing import List


from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum as PYEnum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.utils import CreatedModel
from db import Base, DB


class User(CreatedModel):
    # @classmethod
    # async def get_by_name(cls, name):
    #     query = select(cls).where(cls.name.ilike(f"%{name}%"))
    #     objects = await db.execute(query)
    #     objects = objects.scalars()
    #     if objects:
    #         return objects
    #     else:
    #         return []
    @classmethod
    async def get_by_user_id(cls, id_):
        query = (select(cls)
                 .where(cls.user_id == id_))
        objects: ['User'] = await DB.execute(query)
        object_ = objects.first()
        return object_
    first_name:Mapped[str] = mapped_column(String(255))
    last_name:Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number:Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(unique=True)
    employees : Mapped[List["Employee"]] = relationship(back_populates= 'users')
    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, phone_number={self.phone_number})"
class Customer(CreatedModel):
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete = "SET NULL"), nullable = False)
class OrderStatus(PYEnum):
    progressing = "progressing"
    completed = "completed"
class Post(CreatedModel):
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    file:Mapped[str] = mapped_column(String(255))
    deadline: Mapped[DateTime] = mapped_column(DateTime(timezone = True))
    status: Mapped[OrderStatus] = mapped_column(ENUM(OrderStatus, name = 'order_status_enum'), default=OrderStatus.progressing)
    customer_id: Mapped[int] = mapped_column(ForeignKey(Customer.id, ondelete = "SET NULL"))
    jobs: Mapped[List['Job']] = relationship('Job',secondary = 'posts_jobs', back_populates= 'posts')
class Job(CreatedModel):
    name: Mapped[str] = mapped_column(String(255))
    posts: Mapped[List['Post']] = relationship('Post',secondary = 'posts_jobs', back_populates= 'jobs')
class Employee(CreatedModel):
    experience: Mapped[str] = mapped_column(String(255))
    linkedin: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete = 'SET NULL'), nullable = True)
    rating: Mapped[str] = mapped_column(String(255))
    CV: Mapped[int] = mapped_column(Integer) # file_unique_id dan foydalanamz
    users: Mapped[List["User"]] = relationship(back_populates = 'employees')
    subjobs: Mapped[List['Subjob']] = relationship("Subjob",secondary='subjobs_employees', back_populates = 'employees')
    def __repr__(self):
        return f"Employee(id={self.id}, linkedin={self.linkedin}, description={self.description}, user_id={self.user_id})"
class Subjob(CreatedModel):
    name: Mapped[str] = mapped_column(String(255))
    job_id : Mapped[int] = mapped_column(ForeignKey(Job.id, ondelete = "SET NULL"))
    employees: Mapped[List['Employee']] = relationship("Employee",secondary= 'subjobs_employees' ,back_populates= 'subjobs')

class SubjobEmployee(CreatedModel):
    __tablename__ = 'subjobs_employees'
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id', ondelete = 'SET NULL'))
    subjob_id: Mapped[int] = mapped_column(ForeignKey('subjobs.id', ondelete = 'SET NULL'))
class PostJob(CreatedModel):
    __tablename__ = 'posts_jobs'
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete = 'SET NULL'))
    job_id: Mapped[int] = mapped_column(ForeignKey('jobs.id', ondelete = 'SET NULL'))

metadata = Base.metadata



