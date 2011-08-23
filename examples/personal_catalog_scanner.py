#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Tyler Williams on 2011-04-08

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
"""

# ========================
# = personal_catalog_scanner.py =
# ========================
#
# create a personal catalog by scanning a directory of mp3s with eyeD3
#

import sys
import os
from optparse import OptionParser
import threading
import hashlib
import Queue

from pyechonest import config, catalog

import eyeD3

class IDUploader(threading.Thread):
    def __init__(self, queue, cat_name, cat_type):
        threading.Thread.__init__(self)
        self._queue = queue
        self._catalog = catalog.Catalog(cat_name, cat_type)
    
    def run(self):
        while 1:
            try:
                file_path = self._queue.get(False)
            except Queue.Empty:
                continue

            # is it an mp3?
            if not file_path.endswith(".mp3"):
                self._queue.task_done()
                continue

            # try to pull our data
            fileinfo = {}
            try:
                tag = eyeD3.Tag()
                tag.link(file_path)
                md5_hash = hashlib.md5(open(file_path, "r").read()).hexdigest()
                fileinfo['artist_name'] = tag.getArtist()
                fileinfo['release'] = tag.getAlbum()
                fileinfo['song_name'] = tag.getTitle()
                fileinfo['url'] = file_path
                fileinfo['item_id'] = md5_hash
            except Exception,e:
                print "OH SHIT:",e
                self._queue.task_done()
                continue
            
            cat_item = {'action':'update',
                        'item':fileinfo}
            #pprint(cat_item)
            # post it to the API
            self._catalog.update([cat_item])

            self._queue.task_done()

def scan(directory, queue):
    for folder, subs, files in os.walk(directory):
        for filename in files:
            queue.put(os.path.join(folder, filename))

def main():
    usage = 'usage: %prog [options]  "directory1" "directory2" ... "directoryN"'
    parser = OptionParser(usage=usage)

    parser.add_option("-c", "--catalog",
                      metavar="CATNAME", help="catalog name")

    parser.add_option("-t", "--type",
                      metavar="CATTYPE", help="catalog type")

    parser.add_option("-n", "--threads",
                      metavar="NUMTHREADS", type="int", help="number of worker threads 1 < n < 10")

    (options, args) = parser.parse_args()

    if not options.catalog:
        parser.error("please provide a catalog name with the -c parameter")

    if not options.type:
        parser.error("please specify a catalog type with the -t parameter")

    num_threads = min(max(1, options.threads),10)

    if len(args) < 1:
        parser.error("you must provide at least 1 directory containing mp3s!")
    
    c = catalog.Catalog(options.catalog, options.type)

    queue = Queue.Queue()

    for i in xrange(0,num_threads):
        t = IDUploader(queue, options.catalog, options.type)
        t.setDaemon(True)
        t.start()

    for directory in args:
        print "scanning directory: %s with %d threads" % (directory,num_threads)
        scan(directory, queue)

    queue.join()
    print c.profile
    print "all done!"

if __name__ == "__main__":
    main()
