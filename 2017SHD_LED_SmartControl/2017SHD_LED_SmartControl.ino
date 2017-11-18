#include <string.h>
#include <Arduino.h>
#include <SPI.h>
#include "Servo.h"
#include "Adafruit_BLE.h"
#include "Adafruit_BluefruitLE_SPI.h"
#include "Adafruit_BluefruitLE_UART.h"

#include "BluefruitConfig.h"

#if SOFTWARE_SERIAL_AVAILABLE
#include <SoftwareSerial.h>
#endif

#include <APA102.h>

#define FACTORYRESET_ENABLE         1
#define MINIMUM_FIRMWARE_VERSION    "0.6.6"
#define MODE_LED_BEHAVIOUR          "MODE"

const uint8_t dataPin = 12;
const uint8_t clockPin = 6;

APA102<dataPin, clockPin> ledStrip;

const uint16_t ledCount = 14;

rgb_color colors[ledCount];

const uint8_t brightness = 1;

Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

uint8_t readPacket(Adafruit_BLE *ble, uint16_t timeout);
float parsefloat(uint8_t *buffer);
void printHex(const uint8_t * data, const uint32_t numBytes);

extern uint8_t packetbuffer[];

Servo servo;

const int SWITCH = A2;
const int SERVOPIN = A1;

int ANGLE = 90;
int _CHANGE = 2;

void setup(void)
{

    pinMode(SWITCH, INPUT);
    digitalWrite(SWITCH, HIGH);
    servo.attach(SERVOPIN);

    delay(500);

    if ( !ble.begin(false) )
    {
        while(1);
    }

    if ( FACTORYRESET_ENABLE )
    {
        if ( ! ble.factoryReset() ){
            while(1);
        }
    }

    ble.echo(false);

    while (! ble.isConnected()) {
        delay(500);
    }

    if ( ble.isVersionAtLeast(MINIMUM_FIRMWARE_VERSION) )
    {
        ble.sendCommandCheckOK("AT+HWModeLED=" MODE_LED_BEHAVIOUR);
    }

    ble.setMode(BLUEFRUIT_MODE_DATA);

    colors[0] = rgb_color(255, 0, 0);
    ledStrip.write(colors, ledCount, brightness);
}

void loop(void)
{
    if( digitalRead(SWITCH) == LOW ) {
        ANGLE -= _CHANGE;
    }
    else {
        ANGLE += _CHANGE;
    }
    ANGLE = constrain(ANGLE, 0, 90);
    servo.write(ANGLE);
    char n, inputs[BUFSIZE+1];
    int r;
    int g;
    int b;
    int currentLED;
    while ( ble.available() )
    {
        int c = ble.read();
        if (c == (int)'n') {
            currentLED = ble.read();
            if (currentLED >= ledCount) {
                currentLED = 0;
            }
        }
        else if (c == (int)'r') {
            r = ble.read();
        }
        else if (c == (int)'g') {
            g = ble.read();
        }
        else if (c == (int)'b') {
            b = ble.read(); 
        }
        else {
            continue;
        }
        colors[currentLED] = rgb_color(r,g,b);
        ledStrip.write(colors, ledCount, brightness);
        delay(20);
    }
}
