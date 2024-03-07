import datetime
import time
import vlc
import glob
import random
from collections import deque

def make_player():
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    return player, vlc_instance

def play_song(song, player, vlc_instance):
    # creating a media
    media = vlc_instance.media_new(song)
    # setting media to the player
    player.set_media(media)
    # play the video
    player.play()
    #set player global as active

def choose_song(song_count):
    num = random.randint(0,song_count-1)
    if num in [3]:
        num = choose_song(song_count)
    return num

filenames = glob.glob('songs/*.mp3')

song_count = len(filenames)
chance: int = 3 #adjust for minutes avg between songs

player, vlc_instance = make_player()

last_songs_played = []
song_deque = deque(last_songs_played)

while True:
    now = time.time()
    #Every 60 seconds run this loop
    if int(now) % 60 == 0:
        if not player.is_playing():
            if random.randint(1, chance) == 1:

                song_num = choose_song(song_count)
                while song_num in song_deque:
                    song_num = choose_song(song_count)
                song_deque.append(song_num)
                if len(song_deque) > 3:
                    song_deque.popleft()

                print(f'Last 3 Songs: {song_deque}')

                song = filenames[song_num]
                play_song(song, player, vlc_instance)
                print(f'Playing {song[6:-4:]}')
            else:
                print(f'Skipped')

    time.sleep(1)