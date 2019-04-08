# Youtube TFT Display Board

Fetch data from an Youtube channel using Google API's. For ease of usage and development I decided to use MicroPython running on an ESP32 Wifi board. The TFT Display used was one based on ST7735R driver, but this can easily be ported to other by just using different drivers available [here](https://github.com/adafruit/micropython-adafruit-rgb-display).

![Demo](./images/demo.jpg)

## Hardware

* ESP32 Wemos - [Link](https://www.aliexpress.com/item/1-Set-For-Wemos-MINI-D1-ESP32-WiFi-Bluetooth-For-Wemos-D1-Mini-Esp8266-Module-With/32834982479.html?spm=2114.search0104.3.15.4a9f33d4tNxNyc&ws_ab_test=searchweb0_0,searchweb201602_6_10065_10068_10547_319_10059_10884_317_10548_10887_10696_321_322_10084_453_10083_454_10103_10618_10307_537_536,searchweb201603_6,ppcSwitch_0&algo_expid=87efb6a0-7015-4bc8-aeed-065f61c571d7-2&algo_pvid=87efb6a0-7015-4bc8-aeed-065f61c571d7&transAbTest=ae803_3)
* ST7735R Display - [Link](https://www.aliexpress.com/item/1-8-inch-TFT-LCD-Display-Module-ST7735S-128x160-51-AVR-STM32-ARM-8-16-Bit/32834946843.html?spm=2114.search0104.8.23.16a1b67drvjGg3&transAbTest=ae803_3)
* Jumpers

## 3D Printed case

I added the 3d models for the case that I made. I built it on Tinkercad.

![Case](./images/case.png)

# Instructions

Follow the steps to build you own:

* This is a working in progress, the wiring still missing.

## Setup Youtube API Key

* Go to [Youtube Developers Portal](https://developers.google.com/youtube/v3/docs/).
* Follow the guide "Calling the API"
  * Go to [Developer Console](https://console.developers.google.com/)
  * Go to Credentials 
  * Click on "Create Crendential" then "API Key"
  * Copy that API Key and click on "Restrict Key"
  * Add "Youtube Data API v3" to the restriction list.
  * At the top search bar, search for "Youtube Data API" and enable that API. 

## Setup and install micropython on ESP32

#### Install tools and download micropython binary
```
$ pip3 install adafruit-ampy
$ pip3 install esptool
$ curl -o esp32.bin http://micropython.org/resources/firmware/esp32-20190125-v1.10.bin
```
#### For interactive development (Optional)
```
$ git clone https://github.com/goatchurchprime/jupyter_micropython_kernel.git
$ pip3 install jupyter
$ pip3 install -e jupyter_micropython_kernel
$ python3 -m jupyter_micropython_kernel.install
$ jupyter kernelspec list
```
#### Find serial port
```
$ ls /dev/tty.*
# In my case was /dev/tty.SLAB_USBtoUART
```
#### Clean flash and send micropython binary
```  
$ esptool.py --port /dev/tty.SLAB_USBtoUART erase_flash
$ esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash -z 0x1000 esp32.bin
```

#### Install TFT lib
```
$ curl -o st7735.py https://raw.githubusercontent.com/adafruit/micropython-adafruit-rgb-display/master/st7735.py
$ curl -o rgb.py https://raw.githubusercontent.com/adafruit/micropython-adafruit-rgb-display/master/rgb.py  
$ ampy --port /dev/tty.SLAB_USBtoUART put rgb.py
$ ampy --port /dev/tty.SLAB_USBtoUART put st7735.py
```

#### Install project code

Fill the `config.py` file with you settings for Youtube API, Channel and Wifi connection.

```
$ ampy --port /dev/tty.SLAB_USBtoUART put config.py
$ ampy --port /dev/tty.SLAB_USBtoUART put main.py /main.py
```
