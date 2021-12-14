import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime

class Controller(hass.Hass):

    def initialize(self):
        self.input_device = self.args['input_device']
        self.output_device = self.args['output_device']
        self.setpoint = float(self.args['setpoint'])
        self.deadband = float(self.args['deadband'])
        self.listen_state(self.update, self.input_device, attribute = 'state')
    
    def update(self, entity, attribute, old, new, kwargs):
        self.log(f"Elliot Humidity changed from {old} to {new}")
        new = float(new)
        if new >= self.setpoint:
            self.log(f"turning off elliot's humidifier, setpoint reached at {new}")
            self.turn_off(self.output_device)
        elif new <= self.setpoint - self.deadband:
            self.log(f"turning on elliot's humidifier at {new}")
            self.turn_on(self.output_device)
