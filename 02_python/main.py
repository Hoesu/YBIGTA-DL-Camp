import argparse
import logging
from utils.command_handler import CommandHandler
from utils.command_parser import CommandParser

# TODO 1-1: Use argparse to parse the command line arguments (verbose and log_file).
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--log_path", type=str, default="file_explorer.log")
args = parser.parse_args()

# TODO 1-2: Set up logging and initialize the logger object.
logging.basicConfig(level=logging.INFO, filemode='w', filename=args.log_path,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)
logger.info(f"Input command: {args}")

command_parser = CommandParser(args.verbose)
handler = CommandHandler(command_parser)

while True:
    command = input(">> ")
    handler.execute(command)