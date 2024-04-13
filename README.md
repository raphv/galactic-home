# Galactic Home

![A simulation of the Galactic Home Display](example.svg)

### Displaying data from Home Assistant on the Pimoroni Galactic Unicorn

How the setup works:
 * A Home Assistant [template sensor](https://www.home-assistant.io/docs/configuration/templating/) is used to generate the text and icons to be displayed.
 * Thanks to the Home Assistant [REST API](https://developers.home-assistant.io/docs/api/rest/), this data can be accessed through a single HTTP GET request from http://homeassistant.local:8123/api/states/sensor.galactic_home
 * The Micropython scripts installed on the Galactic Unicorn take this data and display information about your house, the weather, etc.

## Part 1: YAML Configuration Files

This folder contains 2 files:
 * `configuration.yaml` which contains the lines to be added to the main
 * `template.yaml` which contains the display logic to show text and icons on the Galactic Unicorn

In order to change the configuration of the Galactic Unicorn display without the need for a USB cable, the contents of the display are configured in a YAML file in Home Assistant as a [template sensor](https://www.home-assistant.io/docs/configuration/templating/)

This configuration file creates 2 sensors:
 * `sensor.galactic_icons`, which is a list of 11x9 icons displayed in the middle part of the screen
 * `sensor.galactic_home`, which has an attribute named `display` which provides all data used by the galactic unicorn

This configuration allows the Galactic Unicorn to retrieve all data in a single HTTP request.

The configuration provided is an example that displays:
 * The week of the day, using the `now()` function
 * A custom message, created via a [Text Input Helper](https://my.home-assistant.io/redirect/helpers/)
 * The title of the media played on a Media Player
 * The next garbage collection day, using [the Afvalwijzer HACS integration](https://github.com/xirixiz/homeassistant-afvalwijzer)
 * Data from a [local HA calendar](https://www.home-assistant.io/integrations/local_calendar/)
 * Data from temperature sensors
 * Data from Air Quality sensors, with different colours based on different thresholds
 * Three forecasts from [OpenWeatherMap](https://www.home-assistant.io/integrations/openweathermap/)

In order to use the **doorbell** function, you can add it to an automation or script, and trigger the REST command defined in `configuration.yaml`

## Part 2: Micropython files for the Galactic Unicorn

 * `main.py` is the file that is loaded when the Galactic Unicorn launches. It does nothing except call the next Python file.
 * `galactichome.py` contains the main application logic.
 * `gh_visual_assets.py` contains additional assets, such as the font used for the clock digits and the HTML code that shows when querying the Galactic Unicorn over the web.
 * `gh_config.py` where you configure your WiFi network details and the hostname for Home Assistant, among others. You need to generate an API key a.k.a. [long-lived access token](https://www.home-assistant.io/docs/authentication/#your-account-profile) in Home Assistant to put in this file.
 * `wave_player.py` a wrapper to play wave files on the Unicorn. Relies on the files inside the `lib` folder.

Additional files (batteries not included, sorry!) are needed to make it work:
 * Wave files for different times of the day (must be mono, 16-bit, 22050 Hz). Be careful of the limited space on the Pico W. At 43KB/second and less than a megabyte of free space on the controller, you need to keep the total duration under 20 seconds.
 * A wave file for when someone rings the door

## Part 3: Web-based utilities

 * `icon-maker.html`: A tool to create icon codes for the `galactichome.yaml`
 * `display-simulator.html`: A tool to try out how the display would look like and export it as SVG.

## To-do list

 * Use it as an alarm (similar to the door bell, but using Pimoroni's synthesizer functions)
