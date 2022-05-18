# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)

level = logging.INFO  # logging.DEBUG
formatter = u'[%(asctime)s] %(filename)s:%(lineno)d #%(levelname)-8s %(message)s'
date_format = '%H:%M'

logging.basicConfig(
    level=level,
    format=formatter,
    datefmt=date_format,
)

logger.info("logger started successfully")
