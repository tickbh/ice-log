from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self, Union
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel, Column

from iceslog.core.db import datetime_now

class LogFreqBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    module: str = Field(max_length=255, nullable=False, description="记录模块")
    log_time: int = Field(nullable=False, description="归属时间戳")
    times: int = Field(nullable=False, description="请求次数")
    
class LogFreq(LogFreqBase, table=True):
    create_time: datetime = Field(nullable=False, default_factory=datetime_now, description="创建时间")

    __table_args__ = (
        UniqueConstraint("module", "log_time"),
    )
    
class RecordLog(SQLModel):
    time: datetime = None
    log_level: int
    trace_id: str
    uid: int
    content: str
    exid: str = None
    extra: str = None

class RecordLogPublices(SQLModel):
    list: list[RecordLog]
    total: int
    
'''
创建sql, clickhouse
CREATE TABLE log_record (
	log_level Int8,
	trace_id String,
	uid UInt64,
	content String,
	exid String,
	extra String DEFAULT '{}',
	`time` DateTime
) ENGINE = Log;
'''
    
class OneLogVisit(SQLModel):
    module: str
    log_date: datetime
    times: int
    
class LogVisitInfos(SQLModel):
    dates: list[datetime]
    times: list[int]
    module: str
    