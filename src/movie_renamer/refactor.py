import os
import re


class MovieRefactor:
    def __init__(self, folderName):
        self.videoPattern = re.compile(r'.*\.(mp4|mkv|avi|mov|flv|wmv|webm|mpg|mpeg)$', re.IGNORECASE)
        self.imagePattern = re.compile(r'.*\.(jpg|jpeg|png|gif|bmp|tiff|svg|webp|heic)$', re.IGNORECASE)
        self.fileNamePattern = {
            'S01E01': re.compile(r'S(\d{1,2})E(\d{1,2})', re.IGNORECASE),
            'Season 1 Episode 1': re.compile(r'Season (\d+) Episode (\d+)', re.IGNORECASE),
            '1x01': re.compile(r'(\d+)x(\d+)', re.IGNORECASE),
            'S1': re.compile(r'S(\d{1,2})', re.IGNORECASE),
            'Season 1': re.compile(r'Season (\d+)', re.IGNORECASE),
            'Specials': re.compile(r'Specials?\s*(\d{1,2})?', re.IGNORECASE)
        }
        self.folderName = folderName

    def GetVideoFiles(self):
        videoFiles = []
        for root, dirs, files in os.walk(self.folderName):
            for fileName in files:
                if self.videoPattern.match(fileName):
                    videoFiles.append(os.path.join(root, fileName))
        print(videoFiles)
        return videoFiles

    def GetImgFiles(self):
        imgFiles = []
        for root, dirs, files in os.walk(self.folderName):
            for fileName in files:
                if self.imagePattern.match(fileName):
                    imgFiles.append(os.path.join(root, fileName))
        print(imgFiles)
        return imgFiles

    def MatchSeason(self, dirName):
        seasonPatterns = {
            'S1': re.compile(r'S(\d{1,2})', re.IGNORECASE),
            'Season 1': re.compile(r'Season (\d+)', re.IGNORECASE),
            'Specials': re.compile(r'Specials', re.IGNORECASE)
        }

        for formatName, pattern in seasonPatterns.items():
            match = pattern.search(dirName)
            if match:
                if formatName == 'Specials':
                    return f'S00'
                else:
                    seasonNo = int(match.group(1))
                    return f'S{seasonNo:02}'

    def RenameFile(self, filePath, subString, step):
        episodePatterns = {
            'S01E01': re.compile(r'S(\d{1,2})E(\d{1,2})', re.IGNORECASE),
            '01': re.compile(r'\b(\d{2})\b', re.IGNORECASE),
        }

        fileName = os.path.basename(filePath)
        dirPath = os.path.dirname(filePath)
        dirName = os.path.basename(dirPath)
        seasonStr = self.MatchSeason(dirName)

        if subString not in fileName:
            return False

        for formatName, pattern in episodePatterns.items():
            match = pattern.search(fileName)
            formatted = ''
            if match:
                if formatName == 'S01E01':
                    seasonNo = int(match.group(1))
                    # 文件名季号与文件夹季号不一致 or 偏移量不为0
                    if seasonStr != f'S{seasonNo:02}' or step != 0:
                        episodeNo = int(match.group(2)) + step
                        formatted = f'{seasonStr}E{episodeNo:02}'
                if formatName == '01':
                    episodeNo = int(match.group(1)) + step
                    formatted = f'{seasonStr}E{episodeNo:02}'

                if formatted:
                    newFileName = pattern.sub(formatted, fileName, 1)
                    newFilePath = os.path.join(dirPath, newFileName)
                    os.rename(filePath, newFilePath)
                    print(f'Rename {filePath} to {newFilePath} success.')
                    return True
                return False

    def RenameVideoFiles(self, subString='', step=0):
        files = self.GetVideoFiles()
        renameNum = 0
        for filePath in files:
            isSuccess = self.RenameFile(filePath, subString, step)
            if isSuccess == True:
                renameNum += 1
        return renameNum
