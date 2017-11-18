# SHDB17: Make the Sky Blue Again

Using a Adafruit Bluefruit Feather M0, this project controls 14 RGB LEDs and a servo motor to brighten your grey Berlin winter days.

This needs a Linux laptop with a Bluetooth LE capable Bluetooth chip and running BlueZ >= 5.38.

## Installation

For the Python side, install the single requirement with `pip install -r requirements --user`.

For the Feather side, you need the following libraries in your `Arduino/libraries` folder:

* [Adafruit_BluefruitLE_nRF51](https://github.com/adafruit/Adafruit_Python_BluefruitLE)
* [APA102](https://github.com/pololu/apa102-arduino)
* [Servo](https://github.com/arduino-libraries/Servo), if it's not already installed.

You also need to install the Feather board support package.
