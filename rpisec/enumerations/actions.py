# -*- coding: utf-8 -*-

from enum import Enum

from rpisec.enumerations import TextChains


class Actions(Enum):
    STATUS = "status"
    HELP = "help"
    ENABLE = "enable"
    DISABLE = "disable"
    PHOTO = "photo"
    GIF = "gif"
    RESET = "reset"
    REBOOT = "reboot"

    def text_for_action(self):
        return {
            Actions.STATUS: TextChains.CR_STATUS_INFO.value,
            Actions.ENABLE: TextChains.CR_ENABLE_INFO.value,
            Actions.DISABLE: TextChains.CR_DISABLE_INFO.value,
            Actions.PHOTO: TextChains.CR_PHOTO_INFO.value,
            Actions.GIF: TextChains.CR_GIF_INFO.value,
            Actions.REBOOT: TextChains.CR_REBOOT_INFO.value
        }.get(self, TextChains.CT_OTHER_INFO.value)