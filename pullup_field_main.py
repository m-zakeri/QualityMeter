import json
import logging
import os

from qualitymeter.refactoring_opportunities import pullup_field_identification
from qualitymeter.refactoring_opportunities.pullup_field_identification_utils import prettify, print_prettified

# Set the output directory
OUTPUT_DIR = r'.\output'
# Create the directory if it doesn't already exist
if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
# Configure a logger
logging.basicConfig(filename=os.path.join(OUTPUT_DIR, 'app.log'),
                    filemode='w',
                    format='[%(levelname)s] %(asctime)s | %(message)s')
logger = logging.getLogger()
# Pass the logger to the main module
pullup_field_identification.initialize(logger, OUTPUT_DIR)

# Get the code base/backup address from user
path = input('Please enter your codebase/backup path:\n')
# Analyze the codebase and get the result and then prettify it
final_result = prettify(pullup_field_identification.analyze(path), logger=logger)
# Print prettified suggestions
print_prettified(final_result, 0, logger=logger)
# Put the full output in a file
out_path = os.path.join(OUTPUT_DIR, 'output.json')
logger.info(f'Saving the result inside "{out_path}"')
with open(out_path, 'w', encoding='utf-8') as file:
    json.dump(final_result, file, indent=2)
