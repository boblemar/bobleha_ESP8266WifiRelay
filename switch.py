import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .custom_components.const import *
import socket
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import voluptuous as vol

from homeassistant.const import (
    CONF_ALIAS,
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_ROOM,
    SERVICE_TOGGLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_ON,
)

from homeassistant.helpers import (
    collection,
    config_validation as cv,
    entity,
    entity_component,
    event,
    service,
    storage,
)

from homeassistant.components.switch import PLATFORM_SCHEMA

DOMAIN = "bobleha_relaiswifi"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_NAME): cv.string, vol.Required(CONF_IP_ADDRESS): cv.string}
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
    add_entities([bobleha_relaiswifi(name, ip)])


class bobleha_relaiswifi(SwitchEntity):
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
        """Return the display name of this light."""
        _LOGGER.debug(f"Name: {self._name}")
        return self._name

    @property
    def ip(self) -> str:
        """Return the display name of this light."""
        _LOGGER.debug(f"IP: {self._ip}")
        return self._ip

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
        self.__send_tcp_command(COMMAND_ON)
        _LOGGER.debug(f"Turn On")

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        self.turn_on()
        _LOGGER.debug(f"Turn On Async")

    def turn_off(self, **kwargs):
        """Turn the entity off."""
        self.__state_is_on = False
        self.__send_tcp_command(COMMAND_OFF)
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
