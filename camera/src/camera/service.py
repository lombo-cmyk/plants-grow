from time import sleep

from plant_common.env import config
from plant_common.model import LedState
from plant_common.mqtt import MqttClient
from plant_common.service import BaseService

from camera.photocamera import Camera


class Service(BaseService):

    def _pre_run(self, *args, **kwargs):
        camera = Camera(self.logger)
        camera.set_capture_target()
        camera.exit()

    def _subscribe(self, *args, **kwargs):
        self.client.subscribe(
            topic="led/state", handler=self.handle_led_state, payload_class=LedState
        )

    def _setup_scheduled_jobs(self, *args, **kwargs):
        pass

    def handle_led_state(self, client: MqttClient, topic: str, message: LedState):
        if message.state is True:
            self.logger.info("Taking picture")
            sleep(5)  # let camera get the focus after light is turned on
            if config["CAMERA"] is True:
                camera = Camera(self.logger)
                camera.capture()
                camera.exit()
