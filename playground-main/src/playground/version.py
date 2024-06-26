import logging
import requests
from packaging import version

from playground.constants import BASE_DIR

logger = logging.getLogger(__name__)


def latest_version():
    logger.debug("Fetching latest version of Playground.")
    try:
        return version.parse(
            requests.get(
                "https://api.github.com/repos/miny-genie/RTC-mariokart-8-AI/releases/latest",
                timeout=5,
            ).json()["tag_name"]
        )
    
    except Exception:
        return None
    

def current_version():
    with (BASE_DIR / "VERSION").open(encoding="utf-8") as version_file:
        return version.parse(version_file.read().strip())