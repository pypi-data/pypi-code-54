import logging
from braviarc import BraviaRC
from time import sleep

_LOGGER = logging.getLogger(__name__)

ip_address = '192.168.1.102'
braviarc = BraviaRC(ip_address)

pin = '0146'
braviarc.connect(pin, 'my_device_id', 'my device name')
if braviarc.is_connected():
    print(braviarc.get_audio_outputs())
    #print(braviarc.mute_volume(True))
    #print(braviarc.get_volume_info())
    #print(braviarc.mute_volume())
    print(braviarc.get_volume_info())
    for x in braviarc.get_audio_outputs():
        print(braviarc.set_volume_level(.1, x))
        print(braviarc.get_volume_info(x))
