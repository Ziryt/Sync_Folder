import logging
import os
import pause
import croniter
from datetime import datetime
from shutil import copy2, rmtree
from argparse import ArgumentParser
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('Sync logs')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')


def sync_folders(path_from, path_to):
    '''
    Function checks the difference between target and backup folder
    First it removes from backup folder files/folders deleted from target folder
    Then it updates/add new files/folders
    '''

    to_content = os.listdir(path_to)

    for name in to_content:
        name_from = os.path.join(path_from, name)
        name_to = os.path.join(path_to, name)

        if not os.path.exists(name_from):
            if os.path.isfile(name_to):
                os.remove(name_to)
                logger.info(f"Deleted file: {name_to}")
            elif os.path.isdir(name_to):
                rmtree(name_to)
                logger.info(f"Deleted directory: {name_to}")

    from_content = os.listdir(path_from)

    for name in from_content:
        name_from = os.path.join(path_from, name)
        name_to = os.path.join(path_to, name)

        if os.path.isfile(name_from):
            if (not os.path.exists(name_to)
                    or os.path.getmtime(name_from) > os.path.getmtime(name_to)):
                copy2(name_from, name_to)
                logger.info(f'Copied file: {name_from} to {name_to}')
        elif os.path.isdir(name_from):
            if not os.path.exists(name_to):
                os.makedirs(name_to)
                logger.info(f'Created directory: {name_from} to {name_to}')
            sync_folders(name_from, name_to)


def main():
    parser = ArgumentParser(description='This script maintains backup of specific folder '
                                        'with periodical synchronization')

    parser.add_argument('folder', help='path to folder that will be backed up')
    parser.add_argument('destination', help='path were to store backup')
    parser.add_argument('-t', '--time', help='specify desired schedule in CRON format')
    parser.add_argument('-l', '--logs', help='path where to store logs')
    parser.add_argument('-v', '--verbose', help='provide logs info to command line output',
                        action='store_true')

    args = parser.parse_args()

    if args.logs:
        f_handler = TimedRotatingFileHandler(filename=args.logs, when="midnight", backupCount=30, encoding='utf-8')
        f_handler.suffix = "%d-%m-%Y"
        f_handler.setFormatter(formatter)
        logger.addHandler(f_handler)
    if args.verbose:
        s_handler = logging.StreamHandler()
        s_handler.setFormatter(formatter)
        logger.addHandler(s_handler)

    if args.time:
        now = datetime.now()
        cron = croniter.croniter(args.time, now)
        while True:
            pause.until(cron.get_next(datetime))
            logger.info('=====')
            sync_folders(args.folder, args.destination)
    else:
        sync_folders(args.folder, args.destination)


if __name__ == "__main__":
    main()
