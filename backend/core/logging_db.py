from db.models import Log
from sqlalchemy.orm import Session

def log_action(
    db: Session,
    user_id: int,
    action: str,
    table_cible: str,
    item_id: int | None = None,
    detail: str | None = None
):
    log = Log(
        user_id=user_id,
        action=action,
        table_cible=table_cible,
        item_id=item_id,
        detail=detail
    )
    db.add(log)