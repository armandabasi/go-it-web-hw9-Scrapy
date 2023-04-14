from mongoengine import connect
import configparser
import pathlib

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

mongo_user = config.get('DEV_DB', 'USER')
mongodb_pass = config.get('DEV_DB', 'PASSWORD')
db_name = config.get('DEV_DB', 'DB_NAME')
domain = config.get('DEV_DB', 'DOMAIN')

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)

