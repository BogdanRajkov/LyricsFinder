import lyricsgenius as lg
# from ftfy import fix_text
import sounddevice as sd
import soundfile as sf
import acrcloud as acr
from math import floor
import time
import os

"""{'status': {'msg': 'Success', 'code': 0, 'version': '1.0'},
    'metadata': {'music': [{'external_ids': {},
                            'play_offset_ms': 168540,
                            'title': 'Back in Black',
                            'external_metadata': {},
                            'artists': [{'name': 'AC/DC'}],
                            'genres': [{'name': 'Rock'}, {'name': 'Metal/HardRock'}],
                            'release_date': '2014-10-07',
                            'label': 'Epic/Legacy', 
                            'duration_ms': 255640, 
                            'album': {'name': 'Back In Black'}, 
                            'acrid': '4c390710f3d9dfbd509a680e39b78df5', 
                            'result_from': 3, 
                            'score': 100}],
                 'timestamp_utc': '2019-02-03 21:34:15'}, 'cost_time': 4.4179999828339, 'result_type': 0}"""

config = {
        'host': 'http://identify-eu-west-1.acrcloud.com',
        'key': '72df457de33e6b4f42b3705ec90c0823',
        'secret': 'GVfJkLuBoFMCLVChHlb6rG95zhD6idELC8mjETJp',
        'timeout': 10
    }

genius = lg.Genius("oFnb49U1hVNQMaTQXFl-5CGiojGNaI-LE2u0LTDMqqWcI2tQZLOel_BaVPwAcYmh")

sd.default.channels = 2
duration = 5
fs = 44100

os.system('cls')
print('LyricsFinder by Srki & Bobo\n')

print('snimam')
rec_start = time.time()
myrec = sd.rec(int(duration*fs))
sd.wait()

print('pisem u fajl')
sf.write('test.wav', myrec, fs)

print('prepoznajem')
stopwatch = time.time()
song = acr.recognizer(config, 'test.wav')
print('vreme:', time.time() - stopwatch)

if song['status']['msg'] == 'Success':
    # artist_name = fix_text(song['metadata']['music'][0]['artists'][0]['name'])
    # song_name = fix_text(song['metadata']['music'][0]['title'])
    artist_name = song['metadata']['music'][0]['artists'][0]['name']
    song_name = song['metadata']['music'][0]['title']

    play_offset = song['metadata']['music'][0]['play_offset_ms'] / 1000
    song_start = rec_start - play_offset
    song_duration = song['metadata']['music'][0]['duration_ms'] / 1000

    lyrics = genius.search_song(song_name, artist_name)
    print(lyrics)
    if lyrics is None:
        print('Genius nema lyrics :(')
        exit(1)
    else:
        lyrics = lyrics.lyrics
        print(lyrics)
else:
    print('Glup sam, ne nadjoh pesmu :(')
    print('Da ti pustim snimak? (y/n)', end=' ')
    c = input()
    while c not in 'ynYN':
        print('try again:', end=' ')
        c = input()
    if c in 'yY':
        sd.play(myrec)
    exit(1)

# print('press enter to continue...', end='')
# c = input()

prev_line = -1
lyrics = lyrics.split('\n')
line_duration = song_duration / len(lyrics)
repeat = True
while time.time() - song_start < song_duration and repeat == True:
    curr_line = floor((time.time() - song_start) / line_duration)
    if curr_line != prev_line:
        os.system('cls')
        title = artist_name + ' - ' + song_name
        print('-' * len(title), '\n')
        print(title, '\n')
        print('-' * len(title), '\n')
        prev_line = curr_line
        for it in range(len(lyrics)):
            if it == curr_line:
                print('>', end='')
            else:
                print('', end=' ')
            print(lyrics[it])
    repeat = False
