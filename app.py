import asyncio
import datetime
import time

import vallox_websocket_api
from loguru import logger

import _cfg
import _ravendb

config = _cfg.config


def _delay_for_timeout_seconds():
    next_run = datetime.datetime.utcnow() + datetime.timedelta(seconds=config.timeout)
    wait_time = next_run - datetime.datetime.utcnow()
    seconds = wait_time.total_seconds()
    logger.info("Waiting until {next_run} -> {seconds} seconds", next_run=next_run, seconds=seconds)

    time.sleep(seconds)


async def observe_kwl(client: vallox_websocket_api.Client):
    used_metrics = [x["setting"] for x in config.metrics]
    logger.info("fetching {n} metrics", n=len(used_metrics))
    metrics = await client.fetch_metrics(used_metrics)
    _ravendb.store_result(metrics, {x["setting"]: f"{x['explanation']} :{x['range']}" for x in config.metrics})
    logger.info("metrics stored")


async def run():
    client = vallox_websocket_api.Client(config.vallox_ip)
    while True:
        await observe_kwl(client)
        _delay_for_timeout_seconds()


if __name__ == '__main__':
    asyncio.run(run())
