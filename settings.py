import os.path

import class_env

BASE_DIR = os.path.dirname(__file__)

class_env.env_file(os.path.join(BASE_DIR, "etc", "scanner.env")).load()

DEBUG = False
