# -*- coding: utf-8 -*-
from imagepy import IPy, root_dir
from imagepy.core.engine import Free
import os, subprocess, zipfile, shutil

import zipfile, sys, urllib
path = 'https://github.com/Image-Py/imagepy/archive/master.zip'


if sys.version_info[0]==2:
    from urllib import urlretrieve
    from cStringIO import StringIO
else: 
    from urllib.request import urlretrieve
    from io import BytesIO as StringIO

if not os.path.exists('./plugins'):
    os.mkdir('plugins')
if not os.path.exists('./plugins/cache'):
    os.mkdir('plugins/cache')

def Schedule(a,b,c, plg):
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    plg.prgs = (int(per), 100)

class Install(Free):
    title = 'Install Plugins'
    para = {'pkg':''}
    prgs = (0, 100)
    view = [('lab', 'input github url as http://github.com/username/project'),
            (str, 'package', 'pkg', '')]

    def run(self, para=None):
        url = para['pkg']+'/archive/master.zip'
        name = '~'.join(para['pkg'].split('/')[-2:])+'.zip'
        print(url, name)
        IPy.set_info('downloading plugin from %s'%para['pkg'])
        #urlretrieve(url, os.path.join('./plugins/cache', name), 
        #    lambda a,b,c, p=self: Schedule(a,b,c,p))
        zipf = zipfile.ZipFile(os.path.join('./plugins/cache', name))
        zipf.extractall('./plugins/cache')
        destpath = os.path.join('./plugins/', name[:-4])
        if os.path.exists(destpath): shutil.rmtree(destpath)
        os.rename(os.path.join('./plugins/cache/',
            para['pkg'].split('/')[-1]+'-master'), destpath)
        zipf.close()
        IPy.set_info('installing requirement liberies')
        cmds = 'python -m pip install -r %s/requirements.txt'%destpath
        print(cmds)
        subprocess.call(cmds)
        IPy.curapp.reload_plugins(True)

class List(Free):
    title = 'List Plugins'

    def run(self, para=None):
        p = subprocess.Popen("python -m pip list", stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)  
        lst = str(p.stdout.read(), encoding="utf-8").split('\r\n')
        IPy.table('Packages', [[i] for i in lst], ['Packages'])


plgs = [Install, List]