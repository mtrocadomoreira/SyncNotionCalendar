from src.Database import Database
import os
from datetime import datetime
import logging
from configparser import ConfigParser
from glob import glob

if __name__ == "__main__":
    start_datetime = datetime.now()
    cwd = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(cwd, 'logs', f"{start_datetime.strftime('%Y-%m-%dT%H:%M:%S')}.log")

    logging.basicConfig(filename=log_file, filemode='a', level=logging.INFO)

    log_files = glob(os.path.join(cwd, 'logs', '*.log'))


    def file_today(file, date):
        file_day = int(file.split('T')[0].split('-')[-1])
        return file_day != date.day


    to_remove = list(filter(lambda f: file_today(f, start_datetime), log_files))
    for f in to_remove:
        os.remove(os.path.join(cwd, 'logs', f))

    conf = ConfigParser()
    conf.read('config.ini')
    notion_token = conf['GLOBAL']['NOTION_TOKEN']
    apple_calendar = conf['GLOBAL']['APPLE_CALENDAR']
    event_properties = {
        'description': conf['PROPERTIES']['DESCRIPTION'],
        'summary': conf['PROPERTIES']['SUMMARY'],
        'url': conf['PROPERTIES']['URL']
        }
    for key, database_id in conf['DATABASES'].items():
        logging.info(f"Start database {key}")
        db = Database(database_id, notion_token, apple_calendar, event_properties, folder=os.path.join(cwd, 'databases'))
        db.run()
        logging.info(f"End database {key}")
