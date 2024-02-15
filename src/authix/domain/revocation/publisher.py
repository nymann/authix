import logging

from authix.domain.revocation.event import RevocationEvent


class RevocationPublisher:
    async def publish(self, revocation_event: RevocationEvent) -> None:
        logging.debug(f"user '{revocation_event.user_id}' logged out on device '{revocation_event.device_id}'")
