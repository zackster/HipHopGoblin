#!/usr/bin/env python
# encoding: utf-8
"""
get_images.py

Created by Jason Sundram on 2010-02-12.
Updated on 2010-11-03 for pyechonest v4, added threaded downloads.
"""
import glob
import os
import Queue
import shutil
import sys
import threading 
import time
import urllib

from pyechonest.artist import top_hottt
from pyechonest.artist import search

"""
Download images for the Echo Nest's top 1000 hottt artists, and 15 similar artists for each artist.
Files are named by Echo Nest Artist ID. All images that are large enough to look reasonable 
as part of a slideshow or screensaver are copied to a subfolder made in the current working 
directory called "big".

Optionally download images only for a given artist.

Note that we don't use buckets=['images'] to save an API call, since we only get the default
number of images (currently 15) with that call, instead of all of the images the Echo Nest has
(up to 100).
"""

usage = """
usage:
    python get_images.py [optional artist name]
    
    If you don't specify an artist name, images for the top 1000 hottt artists 
    and their similars will be downloaded.
    
    If you do specify an artist name, all images for that artist will be downloaded.
"""

Q = Queue.Queue()

class DownloadThread(threading.Thread):
    """Lightweight thread to download single images stored in the queue (Q)"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        while True:
            url, filename = self.queue.get()
            try:
                print "getting image %s" % filename
                image = urllib.URLopener()
                image.retrieve(url, filename)
            except Exception, e:
                print "skipping %s: %s" % (filename, str(e))
            
            self.queue.task_done()

# Make a pool of threads - 15 is a size that worked well for me.
for i in range(15):
    t = DownloadThread(Q)
    t.setDaemon(True)
    t.start()

# Maintain a record of artists that we already have images for, to avoid multiple downloads.
artists_with_images = set()

def have_images(artist_id):
    """Check to see if we've already downloaded an image for the given artist_id"""
    global artists_with_images
    if not artists_with_images:
        print "Looking for downloaded images ..."
        # See what images we've already got.
        # f: AR00B1I1187FB433EB_00.jpg -> AR00B1I1187FB433EB
        f = lambda x : x[:x.index('_')]
        artists_with_images = set(map(f, glob.glob('AR*_*'))) # only works if script is run in the current directory
        print "Found images for %d artists." % len(artists_with_images)
    return artist_id in artists_with_images

def copy_big(path='.', threshold=1000):
    """Copies the big images into a subfolder called 'big'. Creative, right?"""
    try:
        import Image 
    except ImportError:
        print "copy_big requires PIL. Get it here: http://www.pythonware.com/products/pil/"
        sys.exit(1)
    
    big = os.path.join(path, 'big')
    if not os.path.exists(big):
        os.mkdir(big)
    l = os.listdir(path)
    for i in l:
        try:
            im = Image.open(i)
            if threshold < min(im.size):
                shutil.copyfile(i, os.path.join(big, i))
        except Exception, e:
            print "skipping %s: %s" % (i, e)


def find_artist(artist_name):
    """Return a pyechonest artist for the given artist name."""
    matches = []
    try:
        matches = search(name=artist_name, results=1)
    except Exception, e:
        print "Exception searching for %s: %s" % (artist_name, str(e))
        pass
    if matches:
        return matches[0]
    
    return None

def get_items(items):
    """Accepts a list of tuples (url, filename)"""
    start = time.time()
    for url, filename in items:
        try:
            print "getting image %s" % filename
            image = urllib.URLopener()
            image.retrieve(url, filename)
        except Exception, e:
            print "skipping %s: %s" % (filename, str(e))
    print "Time to get %d images (non-threaded): %s" % (len(items), time.time() - start)

def get_items_threaded(items):
    """ Accepts a list of tuples (url, filename), launches up to 15 threads to retrieve the urls.
        This is faster than a serial download by a factor of 4-8x.
    """
    # Add to queue, the threadpool will get to this as soon as it can.
    for item in items:
        Q.put(item)

def get_images(artist):
    """Retrieve all images for the given pyechonest artist."""
    if have_images(artist.id):
        print "skipping %s, already have images" % artist
        return
    
    images = []
    try:
        # get everything (100 is the max)
        images = artist.get_images(results=100)
    except Exception, e:
        print "EXCEPTION: Couldn't get images for artist %s: %s" % (str(artist), str(e))
        return
     
    items = []
    for i, img in enumerate(images):
        url = img.get('url')
        # There's sometimes some crap after the file extension, most often #flat_doc,
        # e.g. http://userserve-ak.last.fm/serve/_/114442.jpg#flat_doc
        # I remove it here. Would be nice to do this more generally.
        if url:
            ext = url[url.rfind('.'):].replace("#flat_doc", "")
            filename = '%s_%02d%s' % (artist.id, i, ext)
            items.append((url, filename))
    
    get_items_threaded(items)#get_items(items)
    global artists_with_images
    artists_with_images.add(artist)

def download_hottt(count=1000):
    """ Download images for the top 1000 hottt artists, and each of their 15 most similar artists.
        Warning, downloading all these images takes a long time.
    """
    hottest = top_hottt(results=count)
    for i, a in enumerate(hottest):
        print "Processing artist %d of %d" % (i, count)
        get_images(a)
        sims = []
        try:
            sims = a.similar
        except Exception, e:
            print "Couldn't get similars for %s: %s. Sleeping 2." % (str(a), str(e))
            time.sleep(2) # Tired? take a break.
        
        for s in sims:
            get_images(s)
    copy_big()

def download_keyword(desc, count=1000):
    """Similar to download hot, but allows you to specify a description"""
    artists = search(description=desc, results=count, sort='hotttnesss-desc')
    print "Getting images for artists: %s" % str(artists)
    for i, a in enumerate(artists): 
        print "Processing artist %d of %d" % (i, count)
        get_images(a)
        
        for s in a.similar:
            get_images(s)
    
def main():
    if 2 <= len(sys.argv):
        name = ' '.join(sys.argv[1:])
        artist = find_artist(name)
        if artist:
            get_images(artist)
        else:
            print "Couldn't find artist %s" % name
    else:
        download_hottt() #download_keyword(['list', 'of', 'keywords'])
    
    # Wait on the queue until everything has been processed
    Q.join()
    

if __name__ == '__main__':
    main()