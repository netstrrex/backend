from gunicorn.config import Config
from gunicorn.glogging import Logger

from .formatters import create_color_formatter


class GunicornLogger(Logger):
    def setup(self, cfg: Config) -> None:
        super().setup(cfg)
        formatter = create_color_formatter()

        self._set_handler(
            log=self.access_log,
            output=cfg.accesslog,
            fmt=formatter,
        )
        self._set_handler(
            log=self.error_log,
            output=cfg.errorlog,
            fmt=formatter,
        )
