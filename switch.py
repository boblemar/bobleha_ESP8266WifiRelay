import logging
import socket

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers import config_validation as cv
from homeassistant.const import CONF_FRIENDLY_NAME, CONF_IP_ADDRESS, CONF_NAME

import voluptuous as vol

from .const import *

DOMAIN = "bobleha_ESP8266WifiRelay"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Optional(CONF_FRIENDLY_NAME): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType = None,
) -> None:
    """Set up the bobleha_relaiswifi platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    ip = config[CONF_IP_ADDRESS]
    name = config[CONF_NAME]

    # Add devices
    entity = bobleha_ESP8266WifiRelay(name, ip)
    entity.friendlyname = config[CONF_FRIENDLY_NAME]
    add_entities([entity])


class bobleha_ESP8266WifiRelay(SwitchEntity):
    def __init__(self, name, ip) -> None:
        """Initialize an bobleha_relaiswifi."""
        _LOGGER.debug(f"**IP: {ip}")
        _LOGGER.debug(f"**NAME: {name}")
        self._name = name
        self._ip = ip
        self.__state_is_on = False
        self.__port = TCP_DEFAULT_PORT

    @property
    def name(self) -> str:
        """Return the display name of this relay."""
        return self._name

    @property
    def ip(self) -> str:
        """Return the display ip address of this relay."""
        return self._ip

    @property
    def friendlyname(self) -> str:
        """Return the display friendly name of this relay."""
        return self._ip

    @friendlyname.setter
    def friendlyname(self, value):
        """Sets the display friendly name of this relay."""
        self._friendlyname = value

    @property
    def is_on(self) -> bool:
        """Return true if it is on."""
        return self.__state_is_on

    def __send_tcp_command(self, command):
        client = socket.socket()
        client.connect((self.ip, self.__port))
        client.send(command)

    def turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        self.__state_is_on = True
        self.__send_tcp_command(COMMAND_SWITCH1_ON)
        _LOGGER.debug(f"Turn On")

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        self.turn_on()
        _LOGGER.debug(f"Turn On Async")

    def turn_off(self, **kwargs):
        """Turn the entity off."""
        self.__state_is_on = False
        self.__send_tcp_command(COMMAND_SWITCH1_OFF)
        _LOGGER.debug(f"Turn off")

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        self.turn_off()
        _LOGGER.debug(f"Turn off asyc")

    def toggle(self, **kwargs):
        """Toggle the entity."""
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()
        _LOGGER.debug(f"Toggle")

    async def async_toggle(self, **kwargs):
        """Toggle the entity."""
        if self.is_on:
            self.async_turn_off()
        else:
            self.async_turn_on()
        _LOGGER.debug(f"Toggle async")
