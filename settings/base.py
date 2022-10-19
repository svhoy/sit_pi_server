# Standard Library
import sys

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# make sure our apps directory is on the python path
sys.path.append(str(BASE_DIR / "apps"))
