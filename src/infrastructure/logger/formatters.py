from colorlog import ColoredFormatter


def create_color_formatter() -> ColoredFormatter:
    return ColoredFormatter(
        fmt="%(log_color)s%(asctime)s | %(name)-35s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
