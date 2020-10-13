from phue import Bridge
import timeit
from enum import Enum
import time

IP_BRIDGE = '10.0.0.46'

class LightsManager():
    def __init__(self, ip_addr):
        self._bridge = Bridge(ip_addr)
        self._bridge.connect()
        self._transition_time = 1
        self._brightness = 254
        self._state = LIGHTS_STATES.ENABLE.value

    @property
    def is_lights_on(self):
        return self._lights_on

    @is_lights_on.setter
    def is_lights_on(self, value):
        if type(value) == bool:
            self._lights_on = value

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        if value >= 254:
            self._brightness = 254
        elif value <= 1:
            self._brightness = 1
        else:
            self._brightness = value

        for light in self.get_lights():
            light.transitiontime = self._transition_time
            light.brightness = self._brightness

    @property
    def transition_time(self):
        return self._transition_time

    @transition_time.setter
    def transition_time(self, value):
        self._transition_time = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if isinstance(value, LIGHTS_STATES):
            self._state = value.value

    def get_api(self):
        return self._bridge.get_api()

    def get_lights(self):
        return self._bridge.get_light_objects('list')

    def toggle_lights(self):
        for light in self.get_lights():
            is_on = not light.on
            print(is_on)
            light.on = is_on

class ButtonManager():
    def __init__(self):
        self._press_start = 0
        self._press_end = 0

    def reset_press_timer(self):
        self._press_start = 0
        self._press_end = 0

    def start_press_timer(self):
        self._press_start = timeit.default_timer()

    def end_press_timer(self):
        self._press_end = timeit.default_timer()

    def get_press_time(self):
        return self._press_end - self._press_start

class LIGHTS_STATES(Enum):
    BRIGHTNESS = 'brightness'
    ENABLE = 'enable'

lights_manager = LightsManager(IP_BRIDGE)
button_manager = ButtonManager()

def on_button(pressed):
    if pressed:
        button_manager.reset_press_timer()
        button_manager.start_press_timer()
    else:
        button_manager.end_press_timer()
        time_pressed = button_manager.get_press_time()

        print(time_pressed)
        print(lights_manager.state)

        if lights_manager.state == LIGHTS_STATES.BRIGHTNESS.value and time_pressed <= .5:
            lights_manager.state = LIGHTS_STATES.ENABLE

def on_spell(gesture, spell):
    print(spell)

    if lights_manager.state == LIGHTS_STATES.ENABLE.value:
        if spell in ['aguamenti']:
            lights_manager.toggle_lights()

        if spell in ['expelliarmus'] and lights_manager._lights_on:
            lights_manager.state = LIGHTS_STATES.BRIGHTNESS

def on_quaternion(x, y, z, w):
    if lights_manager.state == LIGHTS_STATES.BRIGHTNESS.value:
        print(lights_manager.brightness)
        lights_manager.brightness = w