#Imports
import idsecrets
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.object.eventsub import ChannelPointsCustomRewardRedemptionAddEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
import asyncio
import vlc
import time
import glob
import sqlite3
#! Mutagem for mp3 metadata
#import gradio

#Globals
PLAYER_ACTIVE = False

#Auth System
async def auth():
    #Import Secrets
    app_id = idsecrets.id
    app_secret = idsecrets.secret
    target_scope = [AuthScope.CHANNEL_READ_REDEMPTIONS]
    
    twitch = await Twitch(app_id, app_secret)
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)
    # this will open your default browser and prompt you with the twitch verification website
    token, refresh_token = await auth.authenticate()
    # add User authentication
    await twitch.set_user_authentication(token, target_scope, refresh_token)
    return twitch

async def redem_callback(data: ChannelPointsCustomRewardRedemptionAddEvent):
    print(f'{data.event.user_name} redeemed {data.event.reward.title} message {data.event.user_input}')
    video(filenames[17])


async def event_sub_example(twitch):
    user = await first(twitch.get_users())
    # create eventsub websocket instance and start the client.
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()

    await eventsub.listen_channel_points_custom_reward_redemption_add(user.id, redem_callback)

    try:
        input('press Enter to shut down...')
    except KeyboardInterrupt:
        pass
    finally:
        # stopping both eventsub as well as gracefully closing the connection to the API
        await eventsub.stop()
        await twitch.close()

def video(source):
    global PLAYER_ACTIVE
    # creating a vlc instance
    if not PLAYER_ACTIVE:
        vlc_instance = vlc.Instance()
        # creating a media player
        player = vlc_instance.media_player_new()
        # creating a media
        media = vlc_instance.media_new(source)
        # setting media to the player
        player.set_media(media)
        # play the video
        player.play()
        #set player global as active
        PLAYER_ACTIVE = True

        #get length of song and set event to flip active player bool
        time.sleep(0.5)
        duration = player.get_length()


db = sqlite3.connect("jukequeue.db")


#Add all songs to list
filenames = glob.glob('songs/*.mp3')
#print(filenames)

#Auth with Twitch
print('Authing...')
twitch = asyncio.run(auth())
print(f'Auth Complete...')

asyncio.run(event_sub_example(twitch))