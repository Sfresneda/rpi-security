# -*- coding: utf-8 -*-


from enum import Enum


class TextChains(Enum):
    # Common
    CMMN_UNEXPECTED = "Unexpected❗️"
    CMMN_STATE_NOT_RUNNING = "Not Running 💤"
    CMMN_STATE_ARMED = "Armed 🟢"
    CMMN_STATE_DISARMED = "Disarmed 🔴"
    CMMN_STATE_DISABLED = "Disabled ⚪️"

    CMMN_MOTION_DETECTED = "🚨 Something Detected, reporting…"
    CMMN_SYSTEM_RUNNING = "🚀 System is Running"

    # Change State
    CS_TITLE = "ℹ️ System is now *{0}*"

    # System Status
    ST_TITLE_BOLD = "ℹ️ *System Status*\n"
    ST_CURRENT_STATE_TITLE = "· State *{0}*\n"
    ST_LAST_STATE_TITLE = "· Last State *{0}*\n"
    ST_LAST_CHANGE_TITLE = "· Last Change 🕒 _{0}_\n"
    ST_UPTIME_TITLE = "· Uptime ⏲ _{0}_\n"
    ST_LAST_MAC_DETECTED_TITLE = "· Last MAC Detected: _{0} {1} ago_\n"
    ST_ALARM_TRIGGERED_TITLE_TRUE = "· Alarm is Triggered 🚨\n"
    ST_ALARM_TRIGGERED_TITLE_FALSE = "· Alarm is not Triggered 👀\n"

    # Commands Responses
    CR_STATUS_INFO = "/status: 🚦 Request Status"
    CR_DISABLE_INFO = "/disable: ⚪ Disable Alarm"
    CR_ENABLE_INFO = "/enable: 🟢 Enable Alarm"
    CR_PHOTO_INFO = "/photo: 📸 Take a Photo"
    CR_GIF_INFO = "/gif: 📹 Take a GIF"
    CR_REBOOT_INFO = "/reboot: 🔃 Reboot"
    CT_OTHER_INFO = ""

    CR_TAKING_PHOTO = "📸 Taking a Photo…"
    CR_RECORDING_GIF = "📹 Taking some images to send a GIF…"
    CR_REBOOTING_SYSTEM = "🔃 Rebooting… It will be available in a few seconds"
    CR_UNKNOWN = "⚠️ Command not Found ⚠️"

    # Time Format
    TF_MINUTES = "{0} minutes"
    TF_HOURS = "{0} hours"
    TF_DAYS = "{0} days"

    TF_AND = " and "
    TF_COMMA_SEPARATOR = ", "

    def status_constant_to_enum(self):
        return {
            "notRunning": TextChains.CMMN_STATE_NOT_RUNNING,
            "armed": TextChains.CMMN_STATE_ARMED,
            "disarmed": TextChains.CMMN_STATE_DISARMED,
            "disabled": TextChains.CMMN_STATE_DISABLED
        }.get(self, TextChains.CMMN_UNEXPECTED)
