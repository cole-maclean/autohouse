import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime

class AirQualityControl(hass.Hass):

  def initialize(self):
    self.air_quality_control_sensor = self.args['air_quality_control_sensor']
    self.air_quality_threshold = self.args['air_quality_threshold']
    self.activate_scene = self.args["activate_scene"]
    self.deactivate_scene = self.args["deactivate_scene"]
    self.runtime_seconds = self.args['runtime_seconds']
    self.scene_activaiton_start_time = None

    self.log(f"""Initialzied with sensor {self.air_quality_control_sensor}
    at threshold {self.air_quality_threshold} and runtime
    {self.runtime_seconds} with scene {self.activate_scene}""")

    self.listen_state(self.toggle_control_scene, self.air_quality_control_sensor)

  def toggle_control_scene(self, entity, attribute, old, new, cb_args):
    new = float(new)
    if not self.scene_activaiton_start_time and new >= self.air_quality_threshold:
      self.scene_activaiton_start_time = datetime.now()
      self.turn_on(self.activate_scene)
      self.log(f"""Activating control scene for sensor {self.air_quality_control_sensor}
      at level {new}, above threshold {self.air_quality_threshold}""")
    elif self.scene_activaiton_start_time and new <= self.air_quality_threshold:
      runtime = (datetime.now() - self.scene_activaiton_start_time).total_seconds()
      if runtime > self.runtime_seconds:
        self.turn_on(self.deactivate_scene)
        self.scene_activaiton_start_time = None
        self.log(f"""Deactivating control scene for sensor {self.air_quality_control_sensor}
        at level {new}, runtime = {runtime/60} minutes""")





