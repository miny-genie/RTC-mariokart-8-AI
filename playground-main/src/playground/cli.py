import argparse
import logging
from pathlib import Path
from typing  import Optional

from playground.ui import PlaygroundUI
from playground.config import Config, make_user_dirs
from playground.utils import tb_info
# import playground.web.service as web_service

# Explicit name since this module can be __main__
logger = logging.getLogger("playground.cli")


def main():
    parser = argparse.ArgumentParser(description="Tool for modding Playground.")
    parser.add_argument(
        "--config-file",
        type=Path,
        default=None,
        help="The playground config file to use",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="What level to log at. Default: %(default)s",
    )
    parser.add_argument(
        "--launcher_exe",
        type=Path,
        default=None,
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()
    
    log_format = "%(asctime)s.%(msecs)03d:%(message)s"
    # log_level = logging.getLevelName(args.log_level)
    log_level = args.log_level.upper()
    logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(log_level)
    
    try:
        launch(args, log_level)
    except Exception:    # pylint: disable=broad-except
        logger.critical("%s", tb_info())
        input("Failed to launch Playground. Press Enter to exit...")
        
        
def launch(args, log_level):
    make_user_dirs()
    launcher_exe: Optional[Path] = args.launcher_exe
    exe_dir = None
    if launcher_exe:
        exe_dir = launcher_exe.parent
    
    config = Config.from_path(
        config_path=args.config_file,
        launcher_exe=launcher_exe,
        exe_dir=exe_dir,
    )
    
    # shutdown_callback = web_service.launch_in_thread(config)
    native_ui = PlaygroundUI(config, log_level)
    native_ui.mainloop()
    # shutdown_callback()


# Argparse의 Write 에러 발생
# Pyinstaller의 --noconsole 옵션 활성화 시 발생하는 오류
# 문구를 출력해야 하나 출력할 콘솔이 없어서 발생
# QueueHandler의 log console이랑 연결 확인할 것