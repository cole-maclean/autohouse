import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime

class NoResponseAlarm(hass.Hass):

    def initialize(self):
        self.input_device = self.args['input_device']
        self.output_device = self.args['output_device']
        self.no_response_minutes = self.args['no_response_minutes']
        self.listen_state(self.update, self.input_device, attribute = 'state')
    
    def alarm(self, entity, attribute, old, new, kwargs):
        pass

