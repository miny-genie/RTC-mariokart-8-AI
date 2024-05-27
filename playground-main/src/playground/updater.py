import logging
from urllib.request import urlretrieve
from subprocess import Popen

from .constants import IS_EXE

logger = logging.getLogger(__name__)

LATEST_EXE = (
    
)


def self_update(self_exe):
    if not IS_EXE:
        logger.warning("Tried to update while not an exe. Doing nothing.")
        return
    
    if self_exe is None:
        logger.warning("Passed None as self_exe. Doing nothing.")
        return
    
    exe_dir = self_exe.resolve().parent
    
    new_path = exe_dir / f"{self_exe.stem}.backup{self_exe.suffix}"
    if new_path.exists():
        logger.info("Found previous backup file. Removing.")
        new_path.unlink(missing_ok=True)
        
    logger.info(f"Moving running version to {new_path}")
    self_exe.rename(new_path)
    
    logger.info("Downloading latest version now.")
    urlretrieve(LATEST_EXE, self_exe)
    
    logger.info("Launching new version now.")
    Popen([str(self_exe)])