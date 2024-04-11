#!/usr/bin/env python3
"""
Script for handling Personal Data
"""

from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> List[str]:
    """Returns a log message"""
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message
