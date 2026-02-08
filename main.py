import os
import json
import logging
import sys
import base64

import functions_framework
from backup import _real_backup_mongo_to_gcs as backup_mongo_to_gcs

# Config pulled from Environment Variables (mapped to Secrets)
MONGO_URL = os.environ.get("MONGO_URL")
PYASSISTANTBOT_MONGO_URL = os.environ.get("PYASSISTANTBOT_MONGO_URL")
# DB_NAME = "logistics"
# COLLECTION_NAME = "20260207-hourly-execution"

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - Line:%(lineno)d - %(message)s"
    )
)
logger.addHandler(handler)


@functions_framework.cloud_event
def entrypoint(cloud_event):
    """
    Triggered by a Pub/Sub message via Cloud Scheduler.
    """
    logger.debug(
        dict(
            cloud_event=cloud_event,
            MONGO_URL=MONGO_URL,
            PYASSISTANTBOT_MONGO_URL=PYASSISTANTBOT_MONGO_URL,
        )
    )
    try:
        # 1. Normalize "now" to the start of the hour (UTC)
        # e.g., 2026-02-07 13:48:00 -> 2026-02-07 13:00:00
        # now = datetime.datetime.now(datetime.timezone.utc).replace(
        #     minute=0, second=0, microsecond=0
        # )

        # logger.debug(cloud_event)
        # logger.debug(type(cloud_event))
        # logger.debug(cloud_event.keys())
        # message = cloud_event.get("data", {})
        # logger.debug(message)
        # message = message.get("message", {})
        # logger.debug(message)
        # message = message.get("data")
        # logger.debug(message)

        message = cloud_event.data["message"]["data"]

        if message is None:
            return

        message = base64.b64decode(message).decode("utf-8")
        logger.debug(message)

        data = json.loads(message)
        for r in data:
            logger.debug(r)
            backup_mongo_to_gcs(**r)

    except Exception as e:
        logger.error(f"Critical error during execution: {e}")
