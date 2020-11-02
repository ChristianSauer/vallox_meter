from typing import List, Dict
from typing_extensions import TypedDict

import yaml
import os
import pathlib
from loguru import logger
from dataclasses import dataclass


class Metric(TypedDict):
    setting: str
    explanation: str
    range: str


@dataclass()
class Config:
    timeout: int
    """
    Positive integer, timeout between captures in seconds
    """

    vallox_ip: str
    """
    IP address of the Vallox KWL
    """

    metrics: List[Metric]
    """
    metrics to be ingested
    """

    ravendb_pem_file: str
    """
    File name of the PEM for ravendb. Should be in a directory in this directory
    """

    ravendb_url: str
    """
    url of ravendb
    """

    ravendb_db: str
    "ravendb database, must exist"


default_path = str(pathlib.Path(__file__).parent / "config.yml")

path = os.environ.get("VALLOX_METER_CONFIG_PATH", default_path)
logger.info("loading config from {}", path)

with open(path, "r") as yml_file:
    _data = yaml.safe_load(yml_file)
    config = Config(**_data)

logger.info("config is: {config}", config=config)