## snips-app-sht31
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/snipsco/snips-app-sht31/blob/master/LICENSE)

Action code for the ***Temperature & Humidity [SHT31]*** bundle. It can reply you the current temperature and humidity.

## Usage
***```"Hey snips, please tell me the current temperature?"```***

***```"The current temperature is 24.4 celsius degree."```***

###### OR
***```"Hey snips, what's the temperature in the room in fahrenheit?"```***

***```"The current temperature is 75.8 fahrenheit degree."```***

###### OR
***```"Hey snips, what's the humidity in the room?"```***

***```"The current humidity is 53.25% "```***

## Installation

1. Create a Snips account ***[here](https://console.snips.ai/?ref=Qr4Gq17mkPk)***
2. Create an English assistant in ***[Snips console](https://console.snips.ai/)***
3. Add APP ***Temperature & Humidity [SHT31]***
4. Deploy assistant by ***[Sam](https://snips.gitbook.io/documentation/console/deploy-your-assistant)***
5. (On Pi) Add permission to `_snips-skill` user to access i2c: `sudo usermod -a -G i2c,spi,gpio,audio _snips-skills`
6. (On Pi) Restart snips-skill-server: `sudo systemctl restart snips-skill-server`
7. Have fun ***;-)***

## Acknowledgements

Thanks to [Adafruit](https://github.com/ralf1070/Adafruit_Python_SHT31) providing the lovely SHT31 library.

## Contributing

Please see the [Contribution Guidelines](https://github.com/snipsco/snips-app-sht31/blob/master/CONTRIBUTING.md).

## Copyright

This library is provided by [Snips](https://www.snips.ai) as Open Source software. See [LICENSE](https://github.com/snipsco/snips-app-sht31/blob/master/LICENSE) for more information.
