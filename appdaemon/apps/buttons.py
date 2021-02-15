import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime

class TradfriShortcutButton(hass.Hass):

    def initialize(self):
        self.log(f'Tradfri Button listening to events from id {self.args["button_id"]}')
        self.button_id = self.args["button_id"]
        self.last_scene = -1
        self.click_scenes = self.args['click_scenes']
        self.hold_scene = self.args["hold_scene"]
        self.double_scene = self.args["double_scene"]
        self.listen_event(self.on_button_event, "zha_event")
        self.last_triggered = datetime.now()

    def on_button_event(self, event_name, data, kwargs):
        if (datetime.now() - self.last_triggered).total_seconds() > 0.5:
            self.log(f"event triggered {event_name} with data {data}")
            if data['device_id'] == self.button_id:
                if data['cluster_id'] == 6:
                    new_scene = self.get_scene_cycle()
                    self.turn_on(self.click_scenes[new_scene])
                    self.last_scene = new_scene
                elif data['cluster_id'] == 8:
                    self.turn_on(self.hold_scene)
        self.last_triggered = datetime.now()

    
    def get_scene_cycle(self):
        if (self.last_scene + 1) == len(self.click_scenes):
            return 0
        else:
            return self.last_scene + 1