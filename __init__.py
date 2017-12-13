from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
try:
    from mycroft.skills.audioservice import AudioService
except:
    from mycroft.util import play_mp3
    AudioService = None
from bs4 import BeautifulSoup
import requests


__author__ = 'whohlfeld'

LOGGER = getLogger(__name__)


DLF_URL = 'http://st01.dlf.de/dlf/01/128/mp3/stream.mp3'
DRADIO_URL = 'http://st02.dlf.de/dlf/02/128/mp3/stream.mp3'
NOVA_URL = 'http://st03.dlf.de/dlf/03/128/mp3/stream.mp3'


class RadioSkill(MycroftSkill):
    def __init__(self):
        super(RadioSkill, self).__init__(name="RadioSkill")
        self.audioservice = None

    def initialize(self):
        if AudioService:
            self.audioservice = AudioService(self.emitter)

        whatson_radio_intent = IntentBuilder("WhatsonRadioIntent").\
                         require("WhatsonKeyword").\
                         require("RadioKeyword").build()
        self.register_intent(whatson_dlf_intent, self.handle_whatson_radio_intent)

        radio_intent = IntentBuilder("RadioIntent").\
                        require("RadioKeyword").\
                        require("PlayKeyword").build()
        self.register_intent(dlf_intent, self.handle_radio_intent)

    def handle_whatson_radio_intent(self, message):
        r = requests.get('http://www.deutschlandfunk.de')
        soup = BeautifulSoup(r.text)
        for el in soup.find_all(id='dlf-player-jetzt-im-radio'):
            for a_el in el.find_all('a'):
                self.speak_dialog("currently",
                                  { "station": "dlf", "title": a_el.string})

    def handle_radio_intent(self, message):
        if self.audioservice:
            self.audioservice.play(DLF_URL, message.data['utterance'])
        else:
            self.process = play_mp3(DLF_URL)

    def stop(self):
        pass


def create_skill():
    return RadioSkill()
