import argparse
import refactor
import os

parser = argparse.ArgumentParser()

parser.add_argument('filePath', type=str, help='Path to the file to be renamed.')

args = parser.parse_args()

filePath = args.filePath

if os.path.isdir(filePath):
    refactors = refactor.MovieRefactor(filePath)
    renameNum = refactors.RenameVideoFiles()
else:
    refactor = refactor.MovieRefactor(os.path.dirname(filePath))
    refactor.RenameFile(filePath)