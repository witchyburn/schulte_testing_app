from sqlalchemy.orm import Session
from schemas import TestResultCreate
from models import TestResult
import statistics

def create_test_result(db: Session, test_result: TestResultCreate):
    avg_time = statistics.mean(test_result.times)
    workability_index = test_result.times[0] / avg_time if avg_time > 0 else 0
    mental_stability_index = test_result.times[3] / avg_time if avg_time > 0 else 0

    db_result = TestResult(
        session_id=test_result.session_id,
        times=test_result.times,
        average_time=avg_time,
        workability_index=workability_index,
        mental_stability_index=mental_stability_index
    )

    db.add(db_result)
    db.commit()
    return db_result

def get_test_result(db: Session, result_id: int):
    return db.query(TestResult).filter(TestResult.id == result_id).first()