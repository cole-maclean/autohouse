import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime

class TradfriShortcutButton(hass.Hass):

    def initialize(self):
        self.button_data = self.args['button_data']
        self._build_scene_list()
        self.current_scene_index = -1
        self.hold_scene = self.args["hold_scene"]
        self.last_triggered = datetime.now()
        self.listen_event(self.on_button_event, "zha_event")
        
    def on_button_event(self, event_name, data, kwargs):
        if (datetime.now() - self.last_triggered).total_seconds() > 0.5:
            if data['device_id'] in self.button_data:
                if data['cluster_id'] == 6:
                    new_scene_index = self._get_next_scene_index(self.current_scene_index, data['device_id'])
                    self.turn_on(self.scenes[new_scene_index])
                    self.current_scene_index = new_scene_index
                elif data['cluster_id'] == 8:
                    self.turn_on(self.hold_scene)
                    self.current_scene_index = self.scenes.index(self.hold_scene)
        self.last_triggered = datetime.now()
    
    def _build_scene_list(self):
        self.scenes = []
        for button_id, scenes in self.button_data.items():
            for s in scenes:
                if s not in self.scenes:
                    self.scenes.append(s)

    def _get_next_scene_index(self, current_index, button_id):
        if (current_index + 1) == len(self.scenes):
            next_scene_index = 0
        else:
            next_scene_index = current_index + 1

        if self.scenes[next_scene_index] in self.button_data[button_id]:
            return next_scene_index
        else:
            return self._get_next_scene_index(next_scene_index, button_id)