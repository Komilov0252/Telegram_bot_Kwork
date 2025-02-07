from sqlalchemy import String, ForeignKey, Table, Column, DateTime, Integer, select, BigInteger
from typing import List


from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum as PYEnum
from sqlalchemy.orm import Mapped, joinedload
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
        query = (select(cls.id)
                 .where(cls.user_id == id_))
        objects: ['User'] = await DB.execute(query)
        object_ = objects.first()
        return object_
    first_name:Mapped[str] = mapped_column(String(255), nullable = True)
    last_name:Mapped[str] = mapped_column(String(255), nullable=True)
    username:Mapped[str] = mapped_column(String(255), nullable = True)
    phone_number:Mapped[str] = mapped_column(String(255), nullable=True)
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
    title: Mapped[str] = mapped_column(String(255), nullable = True)
    description: Mapped[str] = mapped_column(String(255), nullable = True)
    file:Mapped[str] = mapped_column(String(255), nullable = True)
    deadline: Mapped[DateTime] = mapped_column(DateTime(timezone = True))
    status: Mapped[OrderStatus] = mapped_column(ENUM(OrderStatus, name = 'order_status_enum'),default=OrderStatus.progressing)
    customer_id: Mapped[int] = mapped_column(ForeignKey(Customer.id, ondelete = "SET NULL"))
    jobs: Mapped[List['Job']] = relationship('Job',secondary = 'posts_jobs', back_populates= 'posts')
class Job(CreatedModel):
    @classmethod
    async def get_name_id(cls):
        query = (select(cls.name, cls.id))
        objects: ['Job'] = await DB.execute(query)
        object_ = objects.all()
        return object_
    name: Mapped[str] = mapped_column(String(255))
    posts: Mapped[List['Post']] = relationship('Post',secondary = 'posts_jobs', back_populates= 'jobs')
class Employee(CreatedModel):
    @classmethod
    async def get_user_id(cls, id_):
        query = (select(User.user_id)
                 .select_from(cls)
                 .join(User, cls.user_id == User.id)
                 .where(User.user_id == id_))
        objects = await DB.execute(query)
        object_ = objects.all()
        if len(object_) == 0:
            return None
        return object_[0]

    @classmethod
    async def get_employee_id_by_user_id(cls, id_):
        query = (select(cls.id)
                 .select_from(cls)
                 .join(User, cls.user_id == User.id)
                 .where(User.user_id == id_))
        objects = await DB.execute(query)
        object_ = objects.all()
        if len(object_) == 0:
            return None
        return object_[0]
    experience: Mapped[str] = mapped_column(String(255), nullable = True)
    linkedin: Mapped[str] = mapped_column(String(255), nullable = True)
    job_id: Mapped[int] = mapped_column(ForeignKey('jobs.id', ondelete = 'SET NULL'))
    user_id: Mapped[BigInteger] = mapped_column( BigInteger, ForeignKey(User.id, ondelete = 'SET NULL'), unique=True)
    rating: Mapped[str] = mapped_column(String(255), nullable = True)
    CV: Mapped[int] = mapped_column(String(255)) # file_unique_id dan foydalanamz
    users: Mapped[List["User"]] = relationship(back_populates = 'employees')
    subjobs: Mapped[List['Subjob']] = relationship("Subjob",secondary='subjobs_employees', back_populates = 'employees')
    def __repr__(self):
        return f"Employee(id={self.id}, linkedin={self.linkedin}, description={self.description}, user_id={self.user_id})"
class Subjob(CreatedModel):
    @classmethod
    async def get_name(cls, id_):
        result = []
        query = (select(cls.name,)
                 .where(cls.job_id == id_))
        objects: ['Job'] = await DB.execute(query)
        object_ = objects.all()
        [result.append(i[0]) for i in object_]
        return result

    @classmethod
    async def get_id_by_name(cls, name_):
        result = []
        query = (select(cls.id, )
                 .where(cls.name == name_))
        objects: ['Subjob'] = await DB.execute(query)
        object_ = objects.first()
        result.append(object_[0])
        return result

    name: Mapped[str] = mapped_column(String(255))
    job_id : Mapped[int] = mapped_column(ForeignKey(Job.id, ondelete = "SET NULL"))
    employees: Mapped[List['Employee']] = relationship("Employee",secondary= 'subjobs_employees' ,back_populates= 'subjobs')

class SubjobEmployee(CreatedModel):
    @classmethod
    async def get_name_by_employee_id(cls, id_):
        result = []
        query = (select(Subjob.name)
                .join(Subjob, Subjob.id == cls.subjob_id)
                .where(cls.employee_id == id_)
                 )

        objects: ['SubjobEmployee'] = await DB.execute(query)
        object_ = objects.all()
        [result.append(i[0]) for i in object_]
        return object_
    __tablename__ = 'subjobs_employees'
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id', ondelete = 'SET NULL'))
    subjob_id: Mapped[int] = mapped_column(ForeignKey('subjobs.id', ondelete = 'SET NULL'))
class PostJob(CreatedModel):
    __tablename__ = 'posts_jobs'
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete = 'SET NULL'))
    job_id: Mapped[int] = mapped_column(ForeignKey('jobs.id', ondelete = 'SET NULL'))

metadata = Base.metadata



