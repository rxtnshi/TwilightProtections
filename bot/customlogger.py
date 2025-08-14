import logging
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(asctime)s %(log_color)s%(levelname)s%(reset)s     %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "DEBUG":    "bold_cyan",
        "INFO":     "bold_blue",
        "WARNING":  "bold_orange",
        "ERROR":    "bold_red",
        "CRITICAL": "bold_red",
    }
))

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)