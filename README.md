# Galactic Home

![A simulation of the Galactic Home Display](example.svg)

### Displaying data from Home Assistant on the Pimoroni Galactic Unicorn

## Part 1: YAML Configuration Files

In order to change the configuration of the Galactic Unicorn display without the need for a USB cable, the contents of the display are configured in a YAML file in Home Assistant as a [template sensor](https://www.home-assistant.io/docs/configuration/templating/)

This configuration file creates 2 sensors:
 * `sensor.galactic_icons`, which is a list of 11x9 icons displayed in the middle part of the screen
 * `sensor.galactic_home`, which has an attribute named `display` which provides all data used by the galactic unicorn

This configuration allows the Galactic Unicorn to retrieve all data in a single HTTP request.

The configuration provided is an example that displays:
 * The week of the day, using the `now()` function
 * The next garbage collection day, using [the Afvalwijzer HACS integration](https://github.com/xirixiz/homeassistant-afvalwijzer)
 * Data from a [local HA calendar](https://www.home-assistant.io/integrations/local_calendar/)
 * Data from temperature sensors
 * Data from Air Quality sensors, with different colours based on different thresholds
 * Three forecasts from [OpenWeatherMap](https://www.home-assistant.io/integrations/openweathermap/)

## Part 2: Micropython files for the Galactic Unicorn

 * `galactichome.py` contains the main application logic.
 * `gh_visual_assets.py` contains additional assets, such as the font used for the clock digits and the HTML code that shows when querying the Galactic Unicorn over the web.
 * `gh_config.py` where you configure your WiFi network details and the hostname for Home Assistant, among others.
 * `wave_player.py` a wrapper to play wave files on the Unicorn. Relies on the files inside the `lib` folder.

Additional files (batteries not included, sorry!) are needed to make it work:
 * Wave files for different times of the day (must be mono, 16-bit, 22050 Hz). Be careful of the limited space on the Pico W. At 43KB/second and less than a megabyte of free space on the controller, you need to keep the total duration under 20 seconds.
 * A wave file for when someone rings the door

## Part 3: Web-based utilities

 * `icon-maker.html`: A tool to create icon codes for the `galactichome.yaml`
 * `display-simulator.html`: A tool to try out how the display would look like and export it as SVG.
