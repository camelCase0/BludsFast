import os

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-3]

config = Config(f'{root_dir}.env')

# DATABASE_URL = f'sqlite:///{root_dir}' + config('POSTGRES_HOST', cast=str) + '.db'

user = config('POSTGRES_USER', cast=str)
password = config('POSTGRES_PASSWORD', cast=str)
host = config('POSTGRES_HOST', cast=str)
db_name = config('POSTGRES_DB', cast=str)

DATABASE_URL = f'postgresql://{user}:{password}@{host}:5432/{db_name}'

# '+config('POSTGRES_PORT', cast=str) + '

SECRET_KEY = config("SECRET_KEY",cast=str)
ALGORITHM = config("ALGORITHM",cast=str)