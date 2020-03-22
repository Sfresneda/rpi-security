# -*- coding: utf-8 -*-

import logging
from datetime import timedelta
from threading import Lock
import time

from rpisec.enumerations import TextChains

logger = logging.getLogger()


def get_readable_delta(then):
    td = timedelta(seconds=time.time() - then)
    days, hours, minutes = td.days, td.seconds // 3600, td.seconds // 60 % 60
    text = TextChains.TF_MINUTES.value.format(minutes)
    if hours > 0:
        text = TextChains.TF_HOURS.value.format(hours) + TextChains.TF_AND.value + text
        if 0 < days:
            text = TextChains.TF_DAYS.value.format(days) + TextChains.TF_COMMA_SEPARATOR.value + text
    return text


class RpisState(object):
    """
    Contains state information about the alarm and handles updates
    """

    def __init__(self, rpis):
        self.rpis = rpis
        self.lock = Lock()
        self.start_time = time.time()
        self.current = 'disarmed'
        self.previous = 'notRunning'
        self.last_change = time.time()
        self.last_packet = time.time()
        self.last_mac = None
        self.triggered = False

    def update_state(self, new_state):
        assert new_state in ['armed', 'disarmed', 'disabled']
        if new_state != self.current:
            with self.lock:
                self.previous = self.current
                self.current = new_state
                self.last_change = time.time()
                self.rpis.telegram_send_message(TextChains.CS_TITLE.value.format(
                    TextChains.status_constant_to_enum(self.current).value)
                )
                logger.info("System is now {0}".format(self.current))

    def update_triggered(self, triggered):
        with self.lock:
            self.triggered = triggered

    def update_last_mac(self, mac):
        with self.lock:
            self.last_mac = mac
            self.last_packet = time.time()

    def check(self):
        if self.current == 'disabled':
            return
        now = time.time()
        if now - self.last_packet > (self.rpis.packet_timeout + 20):
            if self.current != 'armed':
                logger.debug("No packets detected for {0} seconds, arming".format(self.rpis.packet_timeout + 20))
            self.update_state('armed')
        elif now - self.last_packet > self.rpis.packet_timeout:
            logger.debug("Running arp_ping_macs before arming...")
            self.rpis.arp_ping_macs()
        else:
            self.update_state('disarmed')

    def generate_status_text(self):
        status = "".join([
            TextChains.ST_TITLE_BOLD.value,
            TextChains.ST_CURRENT_STATE_TITLE.value.format(TextChains.status_constant_to_enum(self.current).value),
            TextChains.ST_LAST_STATE_TITLE.value.format(TextChains.status_constant_to_enum(self.previous).value),
            TextChains.ST_LAST_CHANGE_TITLE.value.format(get_readable_delta(self.last_change)),
            TextChains.ST_LAST_MAC_DETECTED_TITLE.value.format(self.last_mac, get_readable_delta(self.start_time)),
            TextChains.ST_UPTIME_TITLE.value.format(get_readable_delta(self.start_time)),
            TextChains.ST_ALARM_TRIGGERED_TITLE_TRUE.value if self.triggered else TextChains.ST_ALARM_TRIGGERED_TITLE_FALSE.value
        ])
        return status
