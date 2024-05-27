from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
import json
import logging
from pathlib import Path
import shutil
import time
from typing import Optional, TypeVar

from platformdirs import user_config_dir, user_data_dir, user_cache_dir
from serde.core import field
from serde.de import deserialize
from serde.se import serialize
import serde.json


APP_AUTHOR = "minyGenie"
APP_NAME = "playground"
CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_AUTHOR))
DATA_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
CACHE_DIR = Path(user_cache_dir(APP_NAME, APP_AUTHOR))
SHOW_PACKING_DEFAULT = False

MIN_WIDTH = 1280
MIN_HEIGHT = 720

LAST_INSTALL_BROWSE_DEFAULT = "/"

DEFAULT_COLOR_KEY = "#ff00ff"
DEFAULT_FONT_SIZE = 24
DEFAULT_FONT_FAMILY = "Helvetica"

T = TypeVar("T")

logger = logging.getLogger(__name__)


@dataclass
class CommonTrackerConfig:
    def clone(self: T) -> T:
        return deepcopy(self)


@serialize(rename_all="kebabcase")
@deserialize(rename_all="kebabcase")
@dataclass
class Config:
    config_path: Optional[Path] = field(default=None, metadata={"serde_skip": True})
    dirty: bool = field(default=None, metadata={"serde_skip": True})
    
    launcher_exe: Optional[Path] = field(default=None, metadata={"serde_skip": True})
    exe_dir: Optional[Path] = field(default=None, metadata={"serde_skip": True})
    
    install_dir: Optional[Path] = field(
        default = None,
        # Use custom deserializer to handle None. Unclear why only this field fails
        metadata={"serde_deserializer": lambda v: v if v is None else Path(v)}
    )
    play_version: Optional[str] = field(default=None, skip_if_default=True)
    play_console: bool = field(default=False, skip_if_default=True)
    play_playground: bool = field(default=False, skip_if_default=True)
    play_shortcut: bool = field(default=False, skip_if_default=True)
    geometry: str = field(default=f"{MIN_WIDTH}x{MIN_HEIGHT}", skip_if_default=True)
    # fyi_root
    # fyi_api_token
    theme: Optional[str] = field(default=None, skip_if_default=True)
    last_install_browse: Path = field(
        default=Path(LAST_INSTALL_BROWSE_DEFAULT), skip_if_default=True
    )
    last_tab: Optional[str] = field(default=None, skip_if_default=True)
    tracker_color_key: str = field(default=DEFAULT_COLOR_KEY, skip_if_default=True)
    tracker_font_size: int = field(default=DEFAULT_FONT_SIZE, skip_if_default=True)
    tracker_font_family: str = field(default=DEFAULT_FONT_FAMILY, skip_if_default=True)
    # trackers
    show_packing: bool = field(default=False, skip_if_default=True)
    level_editor_tab: Optional[int] = field(default=None, skip_if_default=True)
    # custom_level_editor_custom_save_formats
    # custom_level_editor_default_save_format
    command_prefix: Optional[list[str]] = field(default=None, skip_if_default=True)
    api_port: int = field(default=9526)
    
    def __post_init__(self):
        if self.exe_dir is None:
            self.exe_dir = Path(__file__).resolve().parent
            
    @classmethod
    def from_path(
        cls,
        config_path: Path = None,
        exe_dir: Optional[Path] = None,
        launcher_exe: Optional[Path] = None,
    ):
        if config_path is None:
            config_path = CONFIG_DIR / "config.json"
        if exe_dir is None:
            exe_dir = Path(__file__).resolve().parent
            
        config = None
        if config_path.exists():
            with config_path.open("r", encoding="utf-8") as config_file:
                try:
                    config = serde.json.from_json(Config, config_file.read())
                    config.config_path = config_path
                except json.decoder.JSONDecodeError:
                    now = int(time.time())
                    backup_path = config_path.with_suffix(f".{now}.json")
                    logger.exception(
                        "Failed to load config. Backing up to %s",
                    )
                    shutil.copyfile(config_path, backup_path)
                    
        if config is None:
            config = Config()
            # config.install_dir = guess_install_dir(exe_dir)
            config.config_path = config_path
            config.save()
                    
        config.launcher_exe = launcher_exe
        config.exe_dir = exe_dir
        
        return config
    
    def _get_tmp_path(self):
        if self.config_path is None:
            raise TypeError("config_path shouldn't be None")
        return self.config_path.with_suffix(f"{self.config_path.suffix}.tmp")
    
    def save(self):
        if self.config_path is None:
            raise TypeError("config_path shouldn't be None")
        self.dirty = False
        
        tmp_path = self._get_tmp_path()
        with tmp_path.open("w", encoding="utf-8") as tmp_file:
            file_content = serde.json.to_json(self, indent=4, sort_keys=True)
            tmp_file.write(file_content)
            
        shutil.copyfile(tmp_path, self.config_path)
        tmp_path.unlink()
                    
                    
                    
                    
                    