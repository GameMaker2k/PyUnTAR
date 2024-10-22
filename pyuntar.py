#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2018 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2018 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2018 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski
    PyUnTar based on iUnTar ver. 4.7 by Kazuki Przyborowski & Josep Sanz Campderros

    $FileInfo: pyuntar.py - Last Update: 1/9/2018 Ver. 4.12.0 RC 1 - Author: cooldude2k $
'''

import os
import sys
import re
import logging as log

if __name__ == '__main__':
    import argparse
    import datetime

__program_name__ = "PyUnTAR"
__project__ = __program_name__
__project_url__ = "https://github.com/GameMaker2k/PyUnTAR"
__version_info__ = (4, 12, 0, "RC 1", 1)
__version_date_info__ = (2024, 10, 22, "RC 1", 1)
__version_date__ = str(__version_date_info__[0])+"."+str(__version_date_info__[
    1]).zfill(2)+"."+str(__version_date_info__[2]).zfill(2)
if(__version_info__[4] is not None):
    __version_date_plusrc__ = __version_date__ + \
        "-"+str(__version_date_info__[4])
if(__version_info__[4] is None):
    __version_date_plusrc__ = __version_date__
if(__version_info__[3] is not None):
    __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(
        __version_info__[2])+" "+str(__version_info__[3])
if(__version_info__[3] is None):
    __version__ = str(
        __version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description="Extract tar files", conflict_handler="resolve", add_help=True)
    argparser.add_argument("-V", "--version", action="version",
                           version=__program_name__+" "+__version__)
    argparser.add_argument(
        "-f", "--tarfile", help="tar file to extract", required=True)
    argparser.add_argument("-v", "--verbose", action="store_true",
                           help="print various debugging information")
    argparser.add_argument(
        "-t", "--list", action="store_true", help="list files only")
    argparser.add_argument(
        "-x", "--extract", action="store_true", help="extract files only")
    argparser.add_argument("-d", "--decompress", default=None,
                           help="decompress file with gzip, bzip2, lzma, or xz")
    argparser.add_argument("-o", "--outputdir",
                           default="./", help="output tar file to dir")
    argparser.add_argument("-c", "--chmod", default=None,
                           help="set chmod vaule for files")
    getargs = argparser.parse_args()


def strip_text_from_file(fhandle, read):
    if(sys.version[0] == "2"):
        temp_text = str(fhandle.read(read))
    if(sys.version[0] >= "3"):
        temp_text = str(fhandle.read(read).decode('ascii'))
    temp_text = temp_text.strip()
    temp_text = ''.join(c for c in temp_text if ord(c) >= 32)
    return str(temp_text)


def no_strip_text_from_file(fhandle, read):
    temp_text = fhandle.read(read)
    return temp_text


def strip_number_from_file(fhandle, read, base=8):
    if(sys.version[0] == "2"):
        temp_num = str(fhandle.read(read))
    if(sys.version[0] >= "3"):
        temp_num = str(fhandle.read(read).decode('ascii'))
    temp_num = temp_num.strip()
    temp_num = ''.join(c for c in temp_num if ord(c) >= 32)
    if(len(str(temp_num)) == 0):
        temp_num = "0"
    return int(temp_num, base)


def check_if_int_is_empty(intval):
    temp_num = intval
    if(len(str(intval)) == 0):
        temp_num = "0"
    return int(temp_num)


def check_compression_support(compression=None):
    if(compression is None):
        return True
    if(compression == "gz"):
        compression = "gzip"
    if(compression == "bzip" or compression == "bz" or compression == "bz2"):
        compression = "bzip2"
    if(compression == "gzip"):
        try:
            import gzip
            return True
        except ImportError:
            return False
    if(compression == "bzip2"):
        try:
            import bz2
            return True
        except ImportError:
            return False
    if(compression == "lzma" or compression == "xz"):
        try:
            import lzma
            return True
        except ImportError:
            return False
    return False


'''
// Python PyUnTAR based on PHP iUnTAR Version 4.7
// license: Revised BSD license
// Kazuki Przyborowski (http://ja.gamemaker2k.org/)
// Josep Sanz Campderros (http://saltos.net/)
'''


def untar(tarfile, outdir="./", chmod=None, extract=True, lsonly=False, compression=None, verbose=False, findfile=None):
    if((verbose is True and extract is True) or (lsonly is True)):
        log.basicConfig(format="%(message)s", level=log.DEBUG)
    TarSize = os.path.getsize(tarfile)
    TarSizeEnd = TarSize - 1024
    TarType = "tar"
    if(extract != True and extract != False):
        extract = False
    if(lsonly != True and lsonly != False):
        lsonly = False
    if(extract is True):
        lsonly = False
    if(compression == "gz"):
        compression = "gzip"
    if(compression == "bzip" or compression == "bz" or compression == "bz2"):
        compression = "bzip2"
    if(compression is not None and compression != "gzip" and compression != "bzip2" and compression != "lzma" and compression != "xz"):
        compression = None
    if(compression == "gzip"):
        try:
            import gzip
        except ImportError:
            compression = None
    if(compression == "bzip2"):
        try:
            import bz2
        except ImportError:
            compression = None
    if(compression == "lzma" or compression == "xz"):
        try:
            import lzma
        except ImportError:
            compression = None
    if(extract is True):
        if(outdir != "" and not os.path.exists(outdir)):
            os.makedirs(outdir, int("0777", 8))
    if(compression is None):
        thandle = open(tarfile, "rb")
    if(compression == "gzip"):
        thandle = gzip.open(tarfile, "rb")
    if(compression == "bzip2"):
        thandle = bz2.BZ2File(tarfile, "rb")
    if(compression == "lzma"):
        thandle = lzma.open(tarfile, "rb")
    thandle.seek(0, 2)
    TarSize = thandle.tell()
    TarSizeEnd = TarSize
    thandle.seek(0, 0)
    i = 0
    if(extract is False):
        FileArray = {}
        i = 0
    outdir = outdir.rstrip('/')+"/"
    if findfile is not None:
        qfindfile = re.escape(findfile)
    if findfile is None:
        qfindfile = None
    thandle.seek(257, 1)
    TarType = strip_text_from_file(thandle, 6)
    if(TarType != "ustar"):
        TarType = "tar"
    thandle.seek(-263, 1)
    while(thandle.tell() < TarSizeEnd):
        FileName = None
        RealFileName = None
        FileDirectory = None
        RealFileDirectory = None
        FileMode = None
        OwnerID = None
        GroupID = None
        FileSize = None
        LastEdit = None
        Checksum = None
        FileType = None
        LinkedFile = None
        FileContent = None
        if(TarType == "ustar"):
            UStar = None
            UStarVer = None
            OwnerName = None
            GroupName = None
            DeviceMajor = None
            DeviceMinor = None
            FilenamePrefix = None
        RealFileName = strip_text_from_file(thandle, 100)
        FileName = str(outdir)+RealFileName
        thandle.seek(56, 1)
        FileType = strip_text_from_file(thandle, 1)
        FileDirectory = os.path.dirname(FileName)
        RealFileDirectory = os.path.dirname(RealFileName)
        thandle.seek(-57, 1)
        if(findfile is not None and FileType != "L" and re.search("/"+qfindfile+"/", RealFileName)):
            thandle.seek(8, 1)
            thandle.seek(8, 1)
            thandle.seek(8, 1)
            FileSize = strip_number_from_file(thandle, 12, 8)
            thandle.seek(12, 1)
            thandle.seek(8, 1)
            FileType = strip_text_from_file(thandle, 12)
            thandle.seek(100, 1)
            thandle.seek(255, 1)
            if(FileType == "0" or FileType == "7" or FileType == "g"):
                thandle.seek(FileSize, 1)
        if(findfile is None or FileType == "L" or re.search("/"+qfindfile+"/", RealFileName)):
            FileMode = strip_text_from_file(thandle, 8)
            if(chmod is None):
                FileCHMOD = int("0"+FileMode[-3:], 8)
            if(chmod is not None):
                FileCHMOD = chmod
            OwnerID = strip_text_from_file(thandle, 8)
            GroupID = strip_text_from_file(thandle, 8)
            FileSize = strip_number_from_file(thandle, 12, 8)
            LastEdit = strip_number_from_file(thandle, 12, 8)
            Checksum = strip_number_from_file(thandle, 8, 8)
            FileType = strip_text_from_file(thandle, 1)
            LinkedFile = strip_text_from_file(thandle, 100)
            if(TarType == "tar"):
                thandle.seek(255, 1)
            if(TarType == "ustar"):
                UStar = strip_text_from_file(thandle, 6)
                UStarVer = strip_text_from_file(thandle, 2)
                OwnerName = strip_text_from_file(thandle, 32)
                GroupName = strip_text_from_file(thandle, 32)
                DeviceMajor = strip_number_from_file(thandle, 8, 8)
                DeviceMinor = strip_number_from_file(thandle, 8, 8)
                FilenamePrefix = strip_text_from_file(thandle, 155)
                thandle.seek(12, 1)
            if(FileType == "L" and FileSize > 0):
                FileName = strip_text_from_file(thandle, FileSize)
                RealFileName = FileName
                FileDirectory = os.path.dirname(FileName)
                RealFileDirectory = os.path.dirname(RealFileName)
                thandle.seek(512-FileSize, 1)
                thandle.seek(100, 1)
                FileMode = strip_text_from_file(thandle, 8)
                if(chmod is None):
                    FileCHMOD = int("0"+FileMode[-3:], 8)
                if(chmod is not None):
                    FileCHMOD = chmod
                OwnerID = strip_text_from_file(thandle, 8)
                GroupID = strip_text_from_file(thandle, 8)
                FileSize = strip_number_from_file(thandle, 12, 8)
                LastEdit = strip_number_from_file(thandle, 12, 8)
                Checksum = strip_number_from_file(thandle, 8, 8)
                FileType = strip_text_from_file(thandle, 1)
                LinkedFile = strip_text_from_file(thandle, 100)
                if(TarType == "tar"):
                    thandle.seek(255, 1)
                if(TarType == "ustar"):
                    UStar = strip_text_from_file(thandle, 6)
                    UStarVer = strip_text_from_file(thandle, 2)
                    OwnerName = strip_text_from_file(thandle, 32)
                    GroupName = strip_text_from_file(thandle, 32)
                    DeviceMajor = strip_number_from_file(thandle, 8, 8)
                    DeviceMinor = strip_number_from_file(thandle, 8, 8)
                    FilenamePrefix = strip_text_from_file(thandle, 155)
                    thandle.seek(12, 1)
        if(((verbose is True and extract is True) or (verbose is False and lsonly is True)) and Checksum != 0):
            if(verbose is True and extract is True):
                log.info(FileName)
            if(verbose is False and lsonly is True):
                log.info(RealFileName)
        if(verbose is True and lsonly is True and Checksum != 0):
            permissions = {'access': {'0': ('---'), '1': ('--x'), '2': ('-w-'), '3': ('-wx'), '4': (
                'r--'), '5': ('r-x'), '6': ('rw-'), '7': ('rwx')}, 'roles': {0: 'owner', 1: 'group', 2: 'other'}}
            permissionstr = ""
            for fmodval in str(FileMode[-3:]):
                try:
                    permissionstr = permissionstr + \
                        permissions['access'][fmodval]
                except KeyError:
                    permissionstr = permissionstr + "---"
            if(FileType == "0" or FileType == "7" or FileType == "g"):
                permissionstr = "-"+permissionstr
            if(FileType == "1"):
                permissionstr = "l"+permissionstr
            if(FileType == "2"):
                permissionstr = "s"+permissionstr
            if(FileType == "5"):
                permissionstr = "d"+permissionstr
            log.info(permissionstr+" "+str(check_if_int_is_empty(OwnerID))+"/"+str(check_if_int_is_empty(GroupID))+" "+str(FileSize).rjust(
                15)+" "+datetime.datetime.utcfromtimestamp(check_if_int_is_empty(LastEdit)).strftime('%Y-%m-%d %H:%M')+" "+RealFileName)
        if((findfile is None or re.search("/"+qfindfile+"/", RealFileName)) and Checksum != 0):
            if(FileType == "0" or FileType == "7" or FileType == "g"):
                if(lsonly is True):
                    thandle.seek(FileSize, 1)
                if(lsonly is False):
                    if(FileSize == 0):
                        FileContent = ""
                    if(FileSize > 0):
                        FileContent = no_strip_text_from_file(
                            thandle, FileSize)
            if(FileType == "1"):
                FileContent = None
            if(FileType == "2"):
                FileContent = None
            if(FileType == "5"):
                FileContent = None
            if(FileType == "0" or FileType == "7" or FileType == "g"):
                if(extract is True):
                    subhandle = open(FileName, "wb+")
                    subhandle.write(FileContent)
                    subhandle.close()
                    os.chmod(FileName, FileCHMOD)
            if(FileType == "1"):
                if(extract is True):
                    os.link(FileName, LinkedFile)
            if(FileType == "2"):
                if(extract is True):
                    os.symlink(LinkedFile, FileName)
            if(FileType == "5"):
                if(extract is True):
                    os.makedirs(FileName, FileCHMOD)
            if(FileType == "0" or FileType == "1" or FileType == "2" or FileType == "5" or FileType == "7" or FileType == "g"):
                if(extract is False):
                    if(lsonly is True):
                        if(TarType == "tar"):
                            FileArray.update({i: {'FileName': FileName, 'RealFileName': RealFileName, 'FileDirectory': FileDirectory, 'RealFileDirectory': RealFileDirectory, 'FileMode': FileMode,
                                             'FileCHMOD': FileCHMOD, 'OwnerID': OwnerID, 'GroupID': GroupID, 'FileSize': FileSize, 'LastEdit': LastEdit, 'Checksum': Checksum, 'FileType': FileType, 'LinkedFile': LinkedFile}})
                        if(TarType == "ustar"):
                            FileArray.update({i: {'FileName': FileName, 'RealFileName': RealFileName, 'FileDirectory': FileDirectory, 'RealFileDirectory': RealFileDirectory, 'FileMode': FileMode, 'FileCHMOD': FileCHMOD, 'OwnerID': OwnerID, 'GroupID': GroupID, 'FileSize': FileSize,
                                             'LastEdit': LastEdit, 'Checksum': Checksum, 'FileType': FileType, 'LinkedFile': LinkedFile, 'UStar': UStar, 'UStarVer': UStarVer, 'OwnerName': OwnerName, 'GroupName': GroupName, 'DeviceMajor': DeviceMajor, 'DeviceMinor': DeviceMinor, 'FilenamePrefix': FilenamePrefix}})
                    if(lsonly is False):
                        if(TarType == "tar"):
                            FileArray.update({i: {'FileName': FileName, 'RealFileName': RealFileName, 'FileDirectory': FileDirectory, 'RealFileDirectory': RealFileDirectory, 'FileMode': FileMode, 'FileCHMOD': FileCHMOD,
                                             'OwnerID': OwnerID, 'GroupID': GroupID, 'FileSize': FileSize, 'LastEdit': LastEdit, 'Checksum': Checksum, 'FileType': FileType, 'LinkedFile': LinkedFile, 'FileContent': FileContent}})
                        if(TarType == "ustar"):
                            FileArray.update({i: {'FileName': FileName, 'RealFileName': RealFileName, 'FileDirectory': FileDirectory, 'RealFileDirectory': RealFileDirectory, 'FileMode': FileMode, 'FileCHMOD': FileCHMOD, 'OwnerID': OwnerID, 'GroupID': GroupID, 'FileSize': FileSize, 'LastEdit': LastEdit,
                                             'Checksum': Checksum, 'FileType': FileType, 'LinkedFile': LinkedFile, 'UStar': UStar, 'UStarVer': UStarVer, 'OwnerName': OwnerName, 'GroupName': GroupName, 'DeviceMajor': DeviceMajor, 'DeviceMinor': DeviceMinor, 'FilenamePrefix': FilenamePrefix, 'FileContent': FileContent}})
        if(extract is False and findfile is None and (i in FileArray and 'FileName' in FileArray[i]) and Checksum != 0):
            i += 1
        if(extract is False):
            if(findfile is not None and re.search("/"+qfindfile+"/", RealFileName) and (i in FileArray and 'FileName' in FileArray[i]) and Checksum != 0):
                i += 1
        if(extract is True):
            if(findfile is not None and re.search("/"+qfindfile+"/", RealFileName) and Checksum != 0):
                i += 1
        if((FileType == "0" or FileType == "7" or FileType == "g") and FileSize > 0):
            CheckSize = 512
            while (CheckSize < FileSize):
                if(CheckSize < FileSize):
                    CheckSize = CheckSize + 512
            SeekSize = CheckSize - FileSize
            thandle.seek(SeekSize, 1)
    thandle.close()
    if(extract is True):
        return True
    if(extract is False):
        return FileArray


'''
// Backwards compatible funtion for PHP iUnTAR
'''


def iuntar(tarfile, outdir="./", chmod=None, extract=True, lsonly=False, compression=None, verbose=False, findfile=None):
    return untar(tarfile, outdir, chmod, extract, lsonly, compression, verbose, findfile)


def pyuntar(tarfile, outdir="./", chmod=None, extract=True, lsonly=False, compression=None, verbose=False, findfile=None):
    return untar(tarfile, outdir, chmod, extract, lsonly, compression, verbose, findfile)


if __name__ == '__main__':
    should_extract = True
    should_list = False
    if(getargs.list is False and getargs.extract is True):
        should_extract = True
        should_list = False
    if(getargs.list is True and getargs.extract is False):
        should_extract = False
        should_list = True
    if(getargs.list is True and getargs.extract is True):
        should_extract = True
        should_list = False
    if(getargs.list is False and getargs.extract is False):
        should_extract = True
        should_list = False
    untar(tarfile=getargs.tarfile, outdir=getargs.outputdir, chmod=getargs.chmod, extract=should_extract,
          lsonly=should_list, compression=getargs.decompress, verbose=getargs.verbose, findfile=None)
