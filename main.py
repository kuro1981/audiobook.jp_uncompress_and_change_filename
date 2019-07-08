#!/usr/bin/env python
# %%
import mutagen
import glob
from zlib import decompress
from zipfile import ZipFile
import os
import re


# %%
def cut_subtitles_in_filename(filename, title):
    ''' cut filename's subtitle
    :param filename: filename
    :param title: search title end and cut this end.
    :return: cut filename string
    '''
    filename, surfix = os.path.splitext(filename)
    match = re.search('^.*' + title, filename)
    # print(match)
    return filename[0:match.end()] + surfix


def main(target_dir, dest_dir, encoding, cutsubtitle=False):
    ''' uncompress audiobook.jp downloaded zipfile
    :param target_dir: zip file existing dir
    :param dest_dir: uncompressed data root dir
    :param encoding: encode multibyte
    :param cutsubtitle: cut filename's subtitle
    '''
    filelist = glob.glob(target_dir+'*.zip')
    with ZipFile(filelist[0]) as z_file:
        alb, aut = '', ''
        files_in_zip = z_file.namelist()
        with z_file.open(files_in_zip[0]) as f:
            m = mutagen.File(f)
            alb = str(m.tags.get('TALB'))
            aut = str(m.tags.get('TPE1'))
        destpath = os.path.join(dest_dir, aut, alb)
        os.makedirs(destpath, exist_ok=True)
        for info in z_file.infolist():
            info.filename = info.filename.encode('cp437').decode(encoding)
            if cutsubtitle:
                info.filename = cut_subtitles_in_filename(info.filename, alb)
            z_file.extract(info, path=destpath)


if __name__ == "__main__":
    target_dir = './audiobookszip/'
    dest_dir = './audiobooks/'
    main(target_dir, dest_dir, encoding='cp932', cutsubtitle=True)
