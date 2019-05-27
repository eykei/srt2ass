'''
Description: Takes two .srt files (one english, one russian) and converts them into a single .ass file,
which allows both subtitles to be displayed simultaneously

Usage:
Enter the path of the .srt files below. the english one first, then the russian one second.
no need to pre-encode to UTF-8

TODO:
auto detect encoding (see chardet library)
support styles (italics, bold)
'''

import shutil, codecs, re

srtpath1 = 'eng.srt'  # the english subtitle
srtpath2 = 'rus.srt'  # the russian subtitle
f1 = codecs.open(srtpath1, 'r+')
f2 = codecs.open(srtpath2, 'r+', encoding='cp1251')
r1 = f1.read().rstrip()
r2 = f2.read().rstrip()

# tags=['<i>','</i>','<b>','</b>']

# r1=re.sub(r'<i>|</i>|<b>|</b>', '', r1)
# r2=re.sub(r'<i>|</i>|<b>|</b>', '', r2)

shutil.copy('template.ass', 'output.ass')

f3 = open('output.ass', 'a', encoding='utf-8')

topSub = r1.split('\n\n')
for event in topSub:
    n, timecode, text = event.split('\n', 2)  # split at first two '\n'
    text = text.replace('\n', ' ')
    start = timecode.split(' --> ')[0]
    end = timecode.split(' --> ')[1]
    start = start[1:-1].replace(',', '.')  # e.g. 00:02:43,382 > 0:02:43.38
    end = end[1:-1].replace(',', '.')
    toWrite = '\nDialogue: 0,%s,%s,Top,%s' % (start, end, text)
    f3.write(toWrite)

botSub = r2.split('\r\n\r\n')
for event in botSub:
    n, timecode, text = event.split('\r\n', 2)
    text = text.replace('\r\n', ' ')
    start = timecode.split(' --> ')[0]
    end = timecode.split(' --> ')[1]
    start = start[1:-1].replace(',', '.')
    end = end[1:-1].replace(',', '.')
    toWrite = '\nDialogue: 0,%s,%s,Bot,%s' % (start, end, text)
    f3.write(toWrite)

f1.close()
f2.close()
f3.close()
