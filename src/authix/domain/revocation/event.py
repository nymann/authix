from datetime import datetime
from datetime import timedelta
from datetime import timezone

from pydantic import BaseModel
from pydantic import UUID4


class RevocationEvent(BaseModel):
    user_id: UUID4
    device_id: str
    invalidate_until: datetime = datetime.now(tz=timezone.utc) + timedelta(minutes=5)

    def message_key(self) -> bytes:
        return str(self.user_id).encode()
