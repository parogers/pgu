"""PGU is a collection of modules for writing games with PyGame.

* gui - A module for creating widget-based interfaces

set the environment variablr "PGU_LOG_LEVEL" to
    - DEBUG
    - INFO
    - WARN
    - ERROR

to get the proper logging level when running. Defaults to "WARN"
[WIP] logging being implemented gradually as the project is brought up to date to 2024
(right now I need some debugging log to find out events not being passed around
in the examples)

"""
import logging
import os

__version__ = '0.22beta1'



level = getattr(logging, os.environ.get("PGU_LOG_LEVEL", "WARN"))

logger = logging.getLogger(__name__)
logger.setLevel(level)
logger.addHandler(logging.StreamHandler())





