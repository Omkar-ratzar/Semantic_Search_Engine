from fastapi import APIRouter
from pydantic import BaseModel
from app.services.search_service import search_query
import time
router = APIRouter()

class QueryIn(BaseModel):
    query: str


@router.post("/")
def run_search(data: QueryIn):
    start=time.perf_counter_ns()
    result=search_query(data.query)
    total_time=time.perf_counter_ns()-start
    result["metrics"]["api_latency_ms"] = round(total_time/1000000, 2)
    return result
