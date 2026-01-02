import uuid
from datetime import datetime
from albayanworker.schemas.document_schemas import ProcessingStatus


class DynamodbController:
    async def get_document_creation(
        report_request_id: uuid, report_creation_table: any
    ):
        response = await report_creation_table.get_item(
            Key={"report_id": report_request_id}
        )
        return (response or {}).get("Item")

    async def update_document_creation(
        report_request_id: uuid,
        new_status: ProcessingStatus,
        report_creation_table: any,
    ):
        await report_creation_table.update_item(
            Key={"report_request_id": str(report_request_id)},
            UpdateExpression="SET request_status = :new_status, update_date = :now",
            ExpressionAttributeValues={
                ":new_status": new_status.value,
                ":now": datetime.now().isoformat(),
            },
        )

    async def get_template_info(
        report_template_id: uuid,
        report_template_table: any,
    ):
        response = await report_template_table.get_item(
            Key={"report_template_id": str(report_template_id)}
        )
        return (response or {}).get("Item")
