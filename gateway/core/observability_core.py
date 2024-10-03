import os

import blinker  # necessary import for elastic apm to work on docker container # noqa
import elasticapm
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from fastapi import FastAPI
from logzero import logger

_apm: elasticapm.Client | None = None
elasticapm.instrument()


ELASTIC_APM_SERVICE_NAME = os.getenv("ELASTIC_APM_SERVICE_NAME")
ELASTIC_APM_SECRET_TOKEN = os.getenv("ELASTIC_APM_SECRET_TOKEN")
ELASTIC_APM_ENVIRONMENT = os.getenv("ELASTIC_APM_ENVIRONMENT")
ELASTIC_APM_SERVER_URL = os.getenv("ELASTIC_APM_SERVER_URL")
ELASTIC_APM_ENABLED = os.getenv("ELASTIC_APM_ENABLED")

def initialize() -> None:
    global _apm
    try:
        apm_config = {
            "SERVICE_NAME": ELASTIC_APM_SERVICE_NAME,
            "SECRET_TOKEN": ELASTIC_APM_SECRET_TOKEN,
            "ENVIRONMENT": ELASTIC_APM_ENVIRONMENT,
            "SERVER_URL": ELASTIC_APM_SERVER_URL,
            "ENABLED": ELASTIC_APM_ENABLED,
        }
        log_config = {**apm_config}
        log_config.pop("SECRET_TOKEN", None)
        logger.info(f"Initializing ElasticAPM with config: {log_config}")
        _apm = make_apm_client(apm_config)
        logger.info(f"ElasticAPM client created: {_apm}")
    except Exception as e:
        logger.error(f"Error initializing ElasticAPM: {e}")
        raise e


def add_client_to_middleware(app: FastAPI) -> None:
    app.add_middleware(ElasticAPM, client=get_apm_client())
    logger.info("ElasticAPM middleware added to app")


def get_apm_client():
    global _apm
    if not _apm:
        initialize()
    return _apm
