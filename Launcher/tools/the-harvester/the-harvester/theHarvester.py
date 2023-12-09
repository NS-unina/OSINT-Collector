#!/usr/bin/env python3
# Note: This script runs theHarvester
import sys

from theHarvester.theHarvester import main

if sys.version_info.major < 3 or sys.version_info.minor < 9:
    print("\033[93m[!] Make sure you have Python 3.9+ installed, quitting.\n\n \033[0m")
    sys.exit(1)

if __name__ == "__main__":
    main()
