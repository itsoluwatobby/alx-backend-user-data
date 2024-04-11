#!/usr/bin/env python3
"""
module filtered_logger.py
"""
import logging
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> List[str]:
    """Returns a log message"""
    return re.sub(r'(?<=^|{})({})(?={}|$)'.format(
        separator, '|'.join(fields), separator), redaction, message)    
