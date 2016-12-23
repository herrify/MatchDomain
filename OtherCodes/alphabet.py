#!/usr/bin/env python3
# @author: johnny
# created: 2016-12-15

import requests
import re
import youtube_dl
import os


def getHtmlText(alpha_url):
    with requests.session() as r:
        return r.get(alpha_url).text


def getAlphaList(text, alpha_url):
    alphas = re.findall(r''' <a data-lightbox="{&quot;galleryId&quot;:&quot;wplightbox&quot;,&quot;width&quot;:460,&quot;height&quot;:494}" class="wplightbox" href="(\S+)">''', text)

    alpha_home = alpha_url.rsplit('/', 1)[0]
    return [ '/'.join([alpha_home, alpha])  for alpha in alphas ]


def getAlphaImgs(text, alpha_url):
    alphas = re.findall(r'''<img alt="(\S+)" src="(\S+)" id=".*" style="position:absolute;left:\d+px;top:\d+px;width:\d+px;height:\d+px;">''', text)

    alpha_home = alpha_url.rsplit('/', 1)[0]
    return [(word, '/'.join([alpha_home, link])) for word, link in alphas]


def downSrcList(alpha_list):
    with youtube_dl.YoutubeDL({'format': 'best'}) as ydl:
        ydl.download(alpha_list)


def fixImgsName(alpha_imgs):
    #filelist = os.listdir()
    for word, link in alpha_imgs:
        linkfile = link.rsplit('/', 1)[1]
        badname = '-'.join([linkfile.rsplit('.', 1)[0], linkfile])
        goodname = '.'.join([word.lower(), linkfile.rsplit('.', 1)[1]])
        if os.path.isfile(badname):
            os.rename(badname, goodname)
        print (badname, goodname)


def mainAlphaGroup(alpha_url):

    downpath = alpha_url.rsplit('/', 1)[1].rsplit('-', 1)[0]
    if not os.path.isdir(downpath): os.mkdir(downpath)
    os.chdir(downpath)

    text = getHtmlText(alpha_url)

    alpha_list = getAlphaList(text, alpha_url)
    downSrcList(alpha_list)

    alpha_imgs = getAlphaImgs(text, alpha_url)
    words, alpha_list = zip(*alpha_imgs)
    downSrcList(alpha_list)
    fixImgsName(alpha_imgs)

    os.chdir('..')


def getAlphaGroup(text, chart_url):
    alphas = re.findall(r'''<a title="" href="(\S+)">\S+</a>''', text)

    alpha_home = chart_url.rsplit('/', 1)[0]
    return [ '/'.join([alpha_home, link]) for link in alphas]


def main():

    chart_url = 'http://www.teachphonics.co.uk/phonics-alphabet-chart.html'

    downpath = 'alphabet'
    if not os.path.isdir(downpath): os.mkdir(downpath)
    os.chdir(downpath)

    text = getHtmlText(chart_url)

    alpha_group = getAlphaGroup(text, chart_url)

    for alpha_url in alpha_group:
        print (alpha_url)
        mainAlphaGroup(alpha_url)
    os.chdir('..')

if __name__ == '__main__':
    main()


