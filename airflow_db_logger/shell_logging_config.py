import sys
from copy import deepcopy
from airflow.config_templates.airflow_local_settings import DEFAULT_LOGGING_CONFIG
import logging

LOG_FORMAT_HEADER = "[%(asctime)s][%(levelname)7s]"
LOG_FORMAT = LOG_FORMAT_HEADER + " %(message)s"


def create_shell_logging_config(
    level=logging.INFO, format: str = LOG_FORMAT, handler_class: str = "airflow_db_logger.handlers.StreamHandler"
):
    LOGGING_CONFIG = deepcopy(DEFAULT_LOGGING_CONFIG)
    LOGGING_CONFIG['version'] = 1
    LOGGING_CONFIG['disable_existing_loggers'] = False
    LOGGING_CONFIG['formatters']['shell'] = {"format": LOG_FORMAT}
    LOGGING_CONFIG['handlers']['console'] = {
        "class": handler_class,
        "formatter": "shell",
    }
    LOGGING_CONFIG['handlers']['task'] = {
        "class": handler_class,
        "formatter": "shell",
    }
    LOGGING_CONFIG['handlers']['processor'] = {
        "class": handler_class,
        "formatter": "shell",
    }
    LOGGING_CONFIG['loggers'] = {
        "airflow.processor": {
            "handlers": ["processor"],
            "level": level,
            "propagate": False,
        },
        "airflow.task": {
            "handlers": ["task"],
            "level": level,
            "propagate": False,
        },
        "flask_appbuilder": {
            "handler": ["console"],
            "level": level,
            "propagate": True,
        },
    }
    return LOGGING_CONFIG
    


SIMPLE_LOGGING_CONFIG = create_shell_logging_config(logging.INFO, handler_class="logging.StreamHandler")
LOGGING_CONFIG = create_shell_logging_config(logging.INFO)
