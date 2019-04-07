import gc
import network
from urequests import get
import st7735
import framebuf
from time import sleep_ms
from rgb import color565
from machine import SPI, Pin
import machine

# Network and API settings
from config import ssid, password, api_key, channel_id

base_url = 'https://www.googleapis.com/youtube/v3'

# Display settings
sck = Pin(26)
miso = Pin(5)
mosi = Pin(22)
cs = Pin(16)
dc = Pin(21)
rst = Pin(17)
w = 128
h = 160
x = 0
y = 0


def get_channel_stat():
    channel_data_url = base_url + '/channels?id=' + \
        channel_id + '&part=statistics&key=' + api_key
    res = get(channel_data_url, stream=True)
    json_data = res.json()
    items = json_data['items']
    channel_data = items[0]
    stats = channel_data['statistics']
    return stats


def get_recent_videos(channel_id, results=10):
    search_url = base_url + '/search?part=snippet&type=video'
    search_url += '&channelId=' + channel_id
    search_url += '&maxResults=' + str(results)
    search_url += '&order=viewCount'
    search_url += '&publishedAfter=2019-01-01T00:00:00Z'
    search_url += '&key=' + api_key
    print(search_url)
    res = get(search_url, stream=True)
    json_data = res.json()
    items = json_data['items']
    return items


def get_video_stat(video_id):
    video_url = base_url + '/videos?part=statistics'
    video_url += '&id=' + video_id
    video_url += '&key=' + api_key
    print(video_url)
    res = get(video_url, stream=True)
    json_data = res.json()
    items = json_data['items']
    data = items[0]
    stat = data['statistics']
    return stat


def connect_wifi():
    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
        return
    station.active(True)
    station.connect(ssid, password)
    i = 0
    while station.isconnected() == False:
        sleep_ms(100)
        i += 1
        if(i == 100):
            machine.reset()
        pass
    print('Connected to wifi')


def main():
    # Connect to wifi
    connect_wifi()
    # Get youtube data
    stats = get_channel_stat()
    video_count = stats['videoCount']
    sub_count = stats['subscriberCount']
    view_count = stats['viewCount']
    print(video_count, sub_count, view_count)
    gc.collect()

    # Get recent videos
    videos = get_recent_videos(channel_id)
    videos = map(lambda video: {
        "id": video['id']['videoId'], "title": video['snippet']['title']}, videos)
    videos = list(videos)
    print(videos)
    gc.collect()

    # Get videos stats
    for video in videos:
        stat = get_video_stat(video['id'])
        video['stat'] = stat
    print(videos)
    gc.collect()

    # Show data on display
    spi = SPI(-1, baudrate=64000000, sck=sck, miso=miso, mosi=mosi)
    display = st7735.ST7735R(spi, dc=dc, cs=cs, rst=rst)
    display.fill(color565(255, 255, 255))
    buf = bytearray(w * h * 2)
    fb = framebuf.FrameBuffer(buf, w, h, framebuf.RGB565)
    gc.collect()

    white = color565(255, 255, 255)
    red = color565(255, 0, 0)
    black = color565(0, 0, 0)
    fb.fill(white)

    fb.fill_rect(0, 0, w, 16, red)
    fb.text('Youtube Stats', 10, 5, white)
    fb.hline(0, 16, h, white)

    fb.fill_rect(0, 17, w, 27, black)
    fb.text(str(view_count) + ' Views', 4, 22, white)
    fb.text(str(sub_count) + ' Subscribers', 4, 32, white)
    # fb.text(str(video_count) + ' Videos',4,50,red)
    fb.hline(0, 44, h, red)

    i = 0
    for video in videos:
        fb.text(video['title'], 0, 48 + i*20, black)
        fb.text(video['stat']['viewCount'] + ' | ' +
                video['stat']['likeCount'], 0, 58 + i*20, red)
        i += 1

    display.blit_buffer(buf, x, y, w, h)
    gc.collect()


try:
    main()
    sleep_ms(5 * 60 * 1000)
    machine.reset()
except:
    sleep_ms(5 * 1000)
    machine.reset()
