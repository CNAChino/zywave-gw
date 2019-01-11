#!/usr/bin/env python3
"""
This module starts the application represented by app object.
"""

import sys
from app import app
import atexit

if __name__ == '__main__':
    sys.exit(app.main(len(sys.argv), sys.argv))
