import os
import logging

from dotenv import load_dotenv
from discord import SyncWebhook

logger = logging.getLogger()
load_dotenv()


def sending_net_liquidity_alert_to_discord(alert_content):
    try:
        webhook = SyncWebhook.partial(os.environ.get("DISCORD_ID"), os.environ.get('DISCORD_KEY'))
        webhook.send(alert_content)
    except Exception as error:
        logger.error("Exception returned when sending a message to discord from liquidity service:", error)
        return {'message': "Failed to contact backend Product service"}
