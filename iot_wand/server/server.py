from iot_wand.mqtt_connections import GestureServer
from iot_wand.btle_scanners import WandScanner
from iot_wand.btle_inerfaces import GestureInterface
import iot_wand.server.settings as _s
import iot_wand.helpers as _h
import time

def main():
    config = _h.yaml_read(_s.PATH_CONFIG)
    conn = GestureServer(config, debug=_s.DEBUG)
    conn.start(async=True, async_callback=lambda _conn: __async_callback(conn, debug=_s.DEBUG))


def __async_callback(conn, debug=False):
    wands = []
    wand_scanner = WandScanner(debug=debug)
    run = True

    try:
        while run:
            if not len(wands):
                wands = [
                    GestureInterface(device, conn).connect()
                    .on('post_connect', lambda interface: None)
                    .on('spell', lambda gesture, spell: on_spell(gesture, spell))
                    .on('position', lambda x, y, w, z: None)
                    .on('post_disconnect', lambda interface: None)
                    for device in wand_scanner.scan()
                ]
            else:
                if not wands[0].connected:
                    wands.clear()
                time.sleep(1)

    except (KeyboardInterrupt, Exception) as e:
        conn.stop()
        for wand in wands:
            wand.disconnect()
        wands.clear()


def on_spell(gesture, spell):
    print('on_spell', gesture, spell)