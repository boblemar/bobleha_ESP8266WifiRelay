"""Constants for bobleha_ESP8266WifiRelay"""

TCP_DEFAULT_PORT = 8080
COMMAND_SWITCH1_ON = bytes.fromhex("A0 01 01 A2")
COMMAND_SWITCH1_OFF = bytes.fromhex("A0 01 00 A1")