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

    $FileInfo: pyuntar.py - Last Update: 1/4/2018 Ver. 4.7.0 RC 1 - Author: cooldude2k $
'''

import os, sys, re;
import logging as log;

if __name__ == '__main__':
 import argparse, datetime;

__program_name__ = "PyUnTAR";
__project__ = __program_name__;
__project_url__ = "https://github.com/GameMaker2k/PyUnTAR";
__version_info__ = (4, 7, 0, "RC 1", 1);
__version_date_info__ = (2018, 1, 4, "RC 1", 1);
__version_date__ = str(__version_date_info__[0])+"."+str(__version_date_info__[1]).zfill(2)+"."+str(__version_date_info__[2]).zfill(2);
if(__version_info__[4]!=None):
 __version_date_plusrc__ = __version_date__+"-"+str(__version_date_info__[4]);
if(__version_info__[4]==None):
 __version_date_plusrc__ = __version_date__;
if(__version_info__[3]!=None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+" "+str(__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

if __name__ == '__main__':
 argparser = argparse.ArgumentParser(description="Extract tar files", conflict_handler="resolve", add_help=True);
 argparser.add_argument("-V", "--version", action="version", version=__program_name__+" "+__version__);
 argparser.add_argument("tarfile", help="tar file to extract");
 argparser.add_argument("-v", "--verbose", action="store_true", help="print various debugging information");
 argparser.add_argument("-t", "--list", action="store_true", help="list files only");
 argparser.add_argument("-x", "--extract", action="store_true", help="extract files only");
 getargs = argparser.parse_args();

def strip_text_from_file(fhandle, read):
 if(sys.version[0]=="2"):
  temp_text = str(fhandle.read(read));
 if(sys.version[0]>="3"):
  temp_text = str(fhandle.read(read).decode('ascii'));
 temp_text = temp_text.strip();
 temp_text = ''.join(c for c in temp_text if ord(c) >= 32);
 return str(temp_text);

def no_strip_text_from_file(fhandle, read):
 temp_text = fhandle.read(read);
 return temp_text;

def strip_number_from_file(fhandle, read, base=8):
 if(sys.version[0]=="2"):
  temp_num = str(fhandle.read(read));
 if(sys.version[0]>="3"):
  temp_num = str(fhandle.read(read).decode('ascii'));
 temp_num = temp_num.strip();
 temp_num = ''.join(c for c in temp_num if ord(c) >= 32);
 return int(temp_num, base);

'''
// Python PyUnTAR based on PHP iUnTAR Version 4.7
// license: Revised BSD license
// Kazuki Przyborowski (http://ja.gamemaker2k.org/)
// Josep Sanz Campderros (http://saltos.net/)
'''
def untar(tarfile, outdir="./", chmod=None, extract=True, lsonly=False, verbose=False, findfile=None):
 if((verbose is True and extract is True) or (lsonly is True)):
  log.basicConfig(format="%(message)s", level=log.DEBUG);
 TarSize = os.path.getsize(tarfile);
 TarSizeEnd = TarSize - 1024;
 if(extract!=True and extract!=False):
  extract = False;
 if(lsonly!=True and lsonly!=False):
  lsonly = False;
 if(extract is True):
  lsonly = False;
 if(extract is True):
  if(outdir!="" and not os.path.exists(outdir)):
   mkdir(outdir, int("0777", 8));
 thandle = open(tarfile, "rb");
 i = 0;
 if(extract is False):
  FileArray = {};
  i = 0;
 outdir = outdir.rstrip('/')+"/";
 if findfile is not None:
  qfindfile = re.escape(findfile);
 if findfile is None:
  qfindfile = None;
 while(thandle.tell()<TarSizeEnd):
  FileName = None;
  FileMode = None;
  OwnerID = None;
  GroupID = None;
  FileSize = None;
  LastEdit = None;
  Checksum = None;
  FileType = None;
  LinkedFile = None;
  FileContent = None;
  FileName = str(outdir)+strip_text_from_file(thandle, 100);
  thandle.seek(56, 1);
  FileType = strip_text_from_file(thandle, 1);
  thandle.seek(-57, 1);
  if(findfile is not None and FileType!="L" and re.search("/"+qfindfile+"/", FileName)):
   thandle.seek(8, 1);
   thandle.seek(8, 1);
   thandle.seek(8, 1);
   FileSize = strip_number_from_file(thandle, 12, 8);
   thandle.seek(12, 1);
   thandle.seek(8, 1);
   FileType = strip_text_from_file(thandle, 12);
   thandle.seek(100, 1);
   thandle.seek(255, 1); 
   if(FileType=="0" or FileType=="7"):
    thandle.seek(FileSize, 1);
  if(findfile is None or FileType=="L" or re.search("/"+qfindfile+"/", FileName)):
   FileMode = strip_text_from_file(thandle, 8);
   if(chmod is None):
    FileCHMOD = int("0"+FileMode[-3:], 8);
   if(chmod is not None):
    FileCHMOD = chmod;
   OwnerID = strip_text_from_file(thandle, 8);
   GroupID = strip_text_from_file(thandle, 8);
   FileSize = strip_number_from_file(thandle, 12, 8);
   LastEdit = strip_number_from_file(thandle, 12, 8);
   Checksum = strip_number_from_file(thandle, 8, 8);
   FileType = strip_text_from_file(thandle, 1);
   LinkedFile = strip_text_from_file(thandle, 100);
   thandle.seek(255, 1);
   if(FileType=="L" and FileSize>0):
    FileName = strip_text_from_file(thandle, FileSize);
    thandle.seek(512-FileSize, 1);
    thandle.seek(100, 1);
    FileMode = strip_text_from_file(thandle, 8);
    if(chmod is None):
     FileCHMOD = int("0"+FileMode[-3:], 8);
    if(chmod is not None):
     FileCHMOD = chmod;
    OwnerID = strip_text_from_file(thandle, 8);
    GroupID = strip_text_from_file(thandle, 8);
    FileSize = strip_number_from_file(thandle, 12, 8);
    LastEdit = strip_number_from_file(thandle, 12, 8);
    Checksum = strip_number_from_file(thandle, 8, 8);
    FileType = strip_text_from_file(thandle, 1);
    LinkedFile = strip_text_from_file(thandle, 100);
    thandle.seek(255, 1);
  if((verbose is True and extract is True) or (verbose is False and lsonly is True)):
   log.info(FileName);
  if(verbose is True and lsonly is True):
   permissions = { 'access': { '0': ('---'), '1': ('--x'), '2': ('-w-'), '3': ('-wx'), '4': ('r--'), '5': ('r-x'), '6': ('rw-'), '7': ('rwx') }, 'roles': { 0: 'owner', 1: 'group', 2: 'other' } };
   permissionstr = "";
   for fmodval in str(FileMode[-3:]):
    permissionstr =  permissions['access'][fmodval] + permissionstr;
   if(FileType=="0" or FileType=="7"):
    permissionstr = "-"+permissionstr;
   if(FileType=="1"):
    permissionstr = "l"+permissionstr;
   if(FileType=="2"):
    permissionstr = "s"+permissionstr;
   if(FileType=="5"):
    permissionstr = "d"+permissionstr;
   log.info(permissionstr+" "+str(int(OwnerID))+"/"+str(int(GroupID))+" "+str(FileSize).rjust(15)+" "+datetime.datetime.utcfromtimestamp(int(LastEdit)).strftime('%Y-%m-%d %H:%M')+" "+FileName);
  if(findfile is None or  re.search("/"+qfindfile+"/", FileName)):
   if(FileType=="0" or FileType=="7"):
    if(lsonly is True):
     thandle.seek(FileSize, 1);
    if(lsonly is False):
     if(FileSize==0):
      FileContent = "";
     if(FileSize>0):
      FileContent = no_strip_text_from_file(thandle, FileSize);
   if(FileType=="1"):
    FileContent = None;
   if(FileType=="2"):
    FileContent = None;
   if(FileType=="5"):
    FileContent = None;
   if(FileType=="0" or FileType=="7"):
    if(extract is True):
     subhandle = open(FileName, "wb+");
     subhandle.write(FileContent);
     subhandle.close();
     os.chmod(FileName, FileCHMOD);
   if(FileType=="1"):
    if(extract is True):
     os.link(FileName, LinkedFile);
   if(FileType=="2"):
    if(extract is True):
     os.symlink(LinkedFile, FileName);
   if(FileType=="5"):
    if(extract is True):
     os.mkdir(FileName, FileCHMOD);
   if(FileType=="0" or FileType=="1" or FileType=="2" or FileType=="5" or FileType=="7"):
    if(extract is False):
     if(lsonly is True):
      FileArray.update({i: {'FileName': FileName, 'FileMode': FileMode, 'OwnerID': OwnerID, 'GroupID': GroupID, 'FileSize': FileSize, 'LastEdit': LastEdit, 'Checksum': Checksum, 'FileType': FileType, 'LinkedFile': LinkedFile}});
     if(lsonly is False):
      FileArray.update({i: {'FileName': FileName, 'FileMode': FileMode, 'OwnerID': OwnerID, 'GroupID': GroupID, 'FileSize': FileSize, 'LastEdit': LastEdit, 'Checksum': Checksum, 'FileType': FileType, 'LinkedFile': LinkedFile, 'FileContent': FileContent}});
  if(extract is False and findfile is None and (i in FileArray and 'FileName' in FileArray[i])):
   i += 1;
  if(extract is False):
   if(findfile is not None and re.search("/"+qfindfile+"/", FileName) and (i in FileArray and 'FileName' in FileArray[i])):
    i += 1;
  if(extract is True):
   if(findfile is not None and re.search("/"+qfindfile+"/", FileName)):
    i += 1;
  if((FileType=="0" or FileType=="7") and FileSize>0):
   CheckSize = 512;
   while (CheckSize<FileSize):
    if(CheckSize<FileSize):
     CheckSize = CheckSize + 512;
   SeekSize = CheckSize - FileSize;
   thandle.seek(SeekSize, 1);
 thandle.close();
 if(extract is True):
  return True;
 if(extract is False):
  return FileArray;

'''
// Backwards compatible funtion for PHP iUnTAR
'''
def iuntar(tarfile, outdir="./", chmod=None, extract=True, lsonly=False, verbose=False, findfile=None):
 return untar(tarfile, outdir, chmod, extract, lsonly, verbose, findfile);

def pyuntar(tarfile, outdir="./", chmod=None, extract=True, lsonly=False, verbose=False, findfile=None):
 return untar(tarfile, outdir, chmod, extract, lsonly, verbose, findfile);

if __name__ == '__main__':
 should_extract = True;
 should_list = False;
 if(getargs.list is False and getargs.extract is True):
  should_extract = True;
  should_list = False;
 if(getargs.list is True and getargs.extract is False):
  should_extract = False;
  should_list = True;
 if(getargs.list is True and getargs.extract is True):
  should_extract = True;
  should_list = False;
 if(getargs.list is False and getargs.extract is False):
  should_extract = True;
  should_list = False;
 untar(getargs.tarfile, extract=should_extract, lsonly=should_list, verbose=getargs.verbose);
