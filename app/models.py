from sqlalchemy import Column, Integer, Uuid, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class TestResult(Base):
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Uuid, index=True)
    times = Column(JSONB)
    average_time = Column(Float)
    workability_index = Column(Float)
    mental_stability_index = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())