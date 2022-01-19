import json
import logging
import os
from typing import List, Tuple, Dict

from antlr4 import *

from qualitymeter.gen.javaLabeled.JavaLexer import JavaLexer
from qualitymeter.gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from .pullup_field_identification_utils import InfoExtractorListener, get_list_of_files, prettify, print_prettified

# A constant denoting output directory
__OUT_DIR = r'.\output'
# A constant to show if we are going to backup extracted info or not
__BACKING = True
# A list of all classes held for back-up
__allClasses = []
# A dictionary to speed up class look ups using class name
__userDefined = {}
# A dictionary to store parent classes and their children
__parentCache = {}
# Declare a name for our logger
__logger = None
# Create a type object for reports Tuple(field name, access level, identical, same access, *list)
T_REPORT = Tuple[str, int, bool, bool,
                 List[Tuple[str, int, bool, int, str, str]], str, str]


def initialize(logger: logging.Logger, output_dir, backup=False, log_level=logging.DEBUG):
    global __logger
    global __OUT_DIR
    __logger = logger
    __OUT_DIR = output_dir
    if not os.path.isdir(__OUT_DIR):
        os.makedirs(__OUT_DIR)
    __logger.setLevel(log_level)
    __BACKING = backup


def __initialize(log_level=logging.DEBUG):
    """
    Initializes an output directory and a logger object
    """
    global __logger
    if not os.path.isdir(__OUT_DIR):
        os.makedirs(__OUT_DIR)
    logging.basicConfig(filename=os.path.join(__OUT_DIR, 'app.log'),
                        filemode='w',
                        format='[%(levelname)s] %(asctime)s | %(message)s')
    __logger = logging.getLogger()
    __logger.setLevel(log_level)


def analyze(path: str) -> Dict[str, List[T_REPORT]]:
    """
    Analyzes the code base and returns a list of possible "pull-up field" candidates.

    :param path: Source path of the codebase or address of a backup.json file
    :return: A dictionary of kind <"parent class name", "refactoring opportunity">
    """
    # Pull globals in
    global __userDefined
    global __parentCache
    global __allClasses
    global __logger
    # Reset the globals
    __userDefined = {}
    __parentCache = {}
    __allClasses = []
    # Index and parse the files if it is a directory
    if os.path.isdir(path):
        _scrape_directory(path)
    # Restore from backup if it is a backup
    elif os.path.basename(path) == 'backup.json':
        _restore_backup(path)
    # Log an error otherwise
    else:
        __logger.error('Invalid path.')
        print('Invalid path!')
        return {}
    # Discover the opportunities
    result = {}
    # Analyze ONLY if the parent is defined within this project
    for item in __parentCache:
        if item not in __userDefined:
            continue
        tmp = _detect_pullup(__parentCache[item])
        tmp.extend(__userDefined[item])
        if len(tmp) > 0:
            result[item] = tmp
    return result


def _scrape_directory(path: str):
    """
    Index all of the .java files and feed it to parser

    :param path: path to the codebase directory
    """
    global __logger
    # Get a list of .java files
    files = get_list_of_files(path)
    # Logs
    print(f'Number of files detected: {len(files)}')
    __logger.info(f'Detected {len(files)} files. Proceeding to parse')
    print('Proceeding to parse...')
    # Parse the files and update the globals
    _parse_files(files)
    print('Finished parsing. Analyzing the data...')
    __logger.info('Finished parsing. Analyzing the data...')


def _restore_backup(path: str):
    """
    Read the backup file and restore class information.

    :param path: path to the backup.json
    """
    # Pull globals in
    global __userDefined
    global __parentCache
    global __allClasses
    global __logger
    # Load the backup.json into program
    __logger.info('Reading backup file.')
    with open(path, 'r', encoding='utf-8') as backup_file:
        __allClasses = json.load(backup_file)
    __logger.info('Decoding backups.')
    # Update globals
    for item in __allClasses:
        # Update search cache
        if item['name'] not in __userDefined:
            __userDefined[item['name']] = (item['path'], item['package'])
        else:
            __logger.warning(f'Duplicate class detected: {item["name"]}')
        # Keep track of classes and their immediate children
        if 'parent' in item:
            parent_name = item['parent']
            if parent_name in __parentCache:
                __parentCache[parent_name].append(item)
            else:
                __parentCache[parent_name] = [item]
    __allClasses = []
    __logger.info('Backup restored successfully')


def _parse_files(file_list: List[str]):
    """
    Parse all of the .java files in the specified directory and all of its subdirectories
    and updates the global parameters.

    :param file_list: List of .java file paths
    """
    # Pull globals in
    global __userDefined
    global __parentCache
    global __allClasses
    global __logger
    # Initiate a walker
    walker = ParseTreeWalker()
    # Iterate over all of the indexed .java files and parse them
    for file in file_list:
        tree = None
        # Generic ANTLR stuff
        try:
            input_stream = FileStream(file, encoding="utf-8")
            lexer = JavaLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = JavaParserLabeled(stream)
            tree = parser.compilationUnit()
        except Exception as e:
            __logger.error(f'File "{file}" is broken', exc_info=True)
            continue
        # Initiate a custom listener
        extractor = InfoExtractorListener()
        # Walk the tree using listener
        walker.walk(extractor, tree)
        # Update globals
        for item in extractor.return_indexed_classes():
            # Update search cache
            item['path'] = file
            if item['name'] not in __userDefined:
                __userDefined[item['name']] = (item['path'], item['package'])
            else:
                __logger.warning(f'Duplicate class detected: {item["name"]}')
            if __BACKING:
                __allClasses.append(item)
            # Keep track of classes and their immediate children
            if 'parent' in item:
                parent_name = item['parent']
                if parent_name in __parentCache:
                    __parentCache[parent_name].append(item)
                else:
                    __parentCache[parent_name] = [item]
    if __BACKING:
        print('Backing up data...')
        tmp_path = os.path.join(__OUT_DIR, 'backup.json')
        __logger.info(f'Creating a backup file at "{tmp_path}"')
        with open(tmp_path, 'w', encoding='utf-8') as file:
            json.dump(__allClasses, file, indent=2)
        __logger.info('Finished backing up.')
    __allClasses = []


def _detect_pullup(classes: List[Dict]) -> List[T_REPORT]:
    """
    Analyze a list of sibling classes and return a pull-up field refactoring
    opportunity report.

    :param classes: A list of sibling classes
    :return: A list of refactoring opportunity reports
    """
    class_count = len(classes)  # Keep track of class count
    # Return an empty list if there are no siblings
    if class_count == 1:
        return []
    # Calculate the intersection of fields within siblings 1 and 2
    duplicates = classes[0]['fields'].keys() & classes[1]['fields'].keys()
    # Return an empty list if there are no intersection
    if len(duplicates) == 0:
        return []
    # Keep doing that with the rest of siblings
    if class_count > 2:
        index = 2
        while index < class_count:
            duplicates &= classes[index]['fields'].keys()
            if len(duplicates) == 0:
                return []
            index += 1
    # If you reach here, it means that you have a few duplicate entries in your siblings
    result = []  # Initialize an actual result list
    # For each of the duplicate fields extract necessary information from classes itself
    # and add it to the report
    for item in duplicates:
        report = []
        access_flag = True
        final_flag = True
        final_lookbehind = classes[0]['fields'][item][1]
        access_level = classes[0]['fields'][item][2]
        for dic in classes:
            tmp = dic['fields'][item]
            report.append((dic['name'], tmp[0], tmp[1],
                          tmp[2], dic['path'], dic['package']))
            if final_lookbehind != tmp[1]:
                final_flag = False
            if access_level != tmp[2]:
                access_flag = False
                if tmp[2] < access_level:
                    access_level = tmp[2]
        # Add the report to results
        result.append((item, access_level, access_flag &
                      final_flag, access_flag, report))
    return result


if __name__ == '__main__':
    __initialize()
    # Get the code base address from user
    directory = input('Please enter your code base address:\n')
    # Analyze the codebase and get the result and then prettify it
    final_result = prettify(analyze(directory), logger=__logger)
    # Print prettified suggestions
    print_prettified(final_result, 0, logger=__logger)
    # Put the full output in a file
    out_path = os.path.join(__OUT_DIR, 'output.json')
    __logger.info(f'Saving the result inside "{out_path}"')
    with open(out_path, 'w', encoding='utf-8') as file:
        json.dump(final_result, file, indent=2)
