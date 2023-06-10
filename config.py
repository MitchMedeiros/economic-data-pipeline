from datetime import date
import os

################ Data Retrieval (src/data/data.py) ################

# Only used if data_type='postgres'. Provide your postgreSQL connection credentials below.
# A note about table formatting: Your tables should have the same names as those listed in the asset dropdown: spy, qqq, vixy.
# The columns should have the lowercase names: date, open, high, low, close, volume.
DATABASE_TYPE = 'postgresql'
USER = ''
PASSWORD = ''
HOST = ''
PORT = ''
DATABASE = ''
connection = f"{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Adjust the date range for the data requested when the app initially loads. Limit the dates that can be chosen.
# Found in src/components/data_inputs.py
calendar_start = date(2021, 1, 1)
calendar_end = date(2022, 12, 31)
minimum_selectable_date = date(2017, 1, 1)
maximum_selectable_date = date(2023, 5, 31)


################ Data Caching (main.py) ################

# Data caching for sharing data amongst callbacks. Specifying 'files' will use the cache_directory provided below.
# If you have a redis database you can choose: 'redis'.
CACHE_TYPE = 'redis'

# Only used if cache_type='files'. Provide the absolute path to the folder you wish to store the cache files in.
CACHE_DIRECTORY = f'{os.getcwd()}/cache'

# Only used if cache_type='redis'. Provide your redis connection credentials below.
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# Only used if cache_type='files'. Choose the maximum number of files to keep in the cache directory before the oldest files are deleted.
CACHE_SIZE = 40

# Only used if cache_type='files'. This allows you to alter the user/group/other permissions for newly created cache files.
# Ex. {'mode':0o770} would give full permissions (rwx) to the owner and group and no permissions to other.
# Newly created files in the cache directory should be owned by the apache user i.e. www-data if using the default permissions below and web hosting.
PERMISSIONS = {'mode': 0o600}


################ Dash Specific Settings (main.py) ################

# Set to True to run the app locally. Set to False for production to only run the app through a wsgi.
RUN_LOCALLY = True

# Only used if run_locally=True. Specify the port to access the app.
PORT_NUMBER = 8050

# Only used if run_locally=True. Primarily for trouble-shooting callback issues and viewing callback process times.
DEBUG_BOOL = True

# Only used if run_locally=True. Suppresses initial callback errors relating to component id if they are intentional.
CALLBACK_SUPPRESS = False

# Serve dash component CSS and Javascript locally or through the https://unpkg.com/ CDN. The default value is True.
LOCALLY_STYLE = True
