import os
import sys

from iot_wand.settings import DEBUG

DEBUG = DEBUG

DIR_BASE = os.path.abspath(os.path.dirname(__file__))
PATH_CONFIG = os.path.join(DIR_BASE, 'clients.yaml')

