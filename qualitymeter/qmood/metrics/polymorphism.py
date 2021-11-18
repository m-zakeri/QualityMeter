from antlr4 import *
from utils.file_reader import FileReader

class Polymorphism:
    def __init__(self, projectPath):
        self.projectPath = projectPath
        for stream in FileReader.getFileStreams(projectPath):
            pass