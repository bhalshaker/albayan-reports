from fastapi import APIRouter
from uuid import UUID
from albayanworker.controllers.report_creation import process_report_creation
from albayanworker.schemas.document_schemas import ReportGenerationSchema

report_creation_router = APIRouter()


@report_creation_router.get(
    "{issue_id}",
    response_model=ReportGenerationSchema,
    title="Retrieve Report Creation Status",
    description="Create report if it is not already created and retrieve the status.",
)
async def retrieve_report(issue_id: UUID) -> ReportGenerationSchema:
    return await process_report_creation(issue_id)
