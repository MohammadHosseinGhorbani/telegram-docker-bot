import yaml
import docker
import i18n
import logging
from jinja2.nativetypes import NativeEnvironment

CONFIG_FILE_LOCATION = '../config.yml'
CONFIG = yaml.load(open(CONFIG_FILE_LOCATION), yaml.CLoader)

dclient = docker.from_env()
jinja = NativeEnvironment()
logger = logging.getLogger(__name__)


def prerun():
    for key, value in yaml.load(open(CONFIG['texts_file']), yaml.CLoader).items():
        i18n.add_translation(key, str(value))

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=[
            logging.FileHandler('logs.txt'),
            logging.StreamHandler()
        ]
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)

