import logging
import logging.config
import sys


import logging
import logging.config
import sys

def setup_logging(settings):
    root = logging.getLogger()

    # wipe anything uvicorn/basicConfig added
    root.handlers.clear()

    log_level = getattr(logging, settings.LOG_LEVEL)

    if settings.ENV == "dev":
        from rich.logging import RichHandler

        handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_level=True,
            show_path=False,  # IMPORTANT
        )

        formatter = logging.Formatter(
            "%(name)s | %(message)s"
        )
        handler.setFormatter(formatter)

    else:
        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        handler.setFormatter(formatter)

    handler.setLevel(log_level)

    root.setLevel(log_level)
    root.addHandler(handler)

    # Optional: quiet noisy libs in prod
    if settings.ENV != "dev":
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("apscheduler").setLevel(logging.WARNING)
