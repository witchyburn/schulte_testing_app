from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TestResultCreate(BaseModel):
    times: list[float]

class TestResultResponse(TestResultCreate):
    id: int
    session_id: str
    average_time: float
    workability_index: float
    mental_stability_index: float
    created_at: datetime
    
    model_config = ConfigDict(from_attributes = True)