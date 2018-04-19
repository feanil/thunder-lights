#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// Center Cloud
#define PIXELS 100
// Window Cloud
//#define NUM_LEDS 60


#define PIN 15

Adafruit_NeoPixel strip = Adafruit_NeoPixel(PIXELS, PIN, NEO_GRB + NEO_KHZ800);

uint8_t intensity = 0;
uint8_t test_index = 0;

void setup() {
    Serial.begin(115200);
    strip.begin();
    strip.show();
    randomSeed(analogRead(0));
}

void loop() {
    if (Serial.available() > 0) {
      intensity = Serial.read();
      pattern_one(intensity);

    }
}

void pattern_one(uint8_t intensity) {
    if(intensity == 0){
      test_index = random(294)+3;
    }
    
    strip.setPixelColor(test_index-3, strip.Color(0,0,0));
    strip.setPixelColor(test_index-2, strip.Color(64,64,64));
    strip.setPixelColor(test_index-1, strip.Color(128,128,128));
    strip.setPixelColor(test_index, strip.Color(intensity,intensity,intensity));
    strip.setPixelColor(test_index+1, strip.Color(intensity,intensity,intensity));
    strip.setPixelColor(test_index+2, strip.Color(intensity,intensity,intensity));
    strip.setPixelColor(test_index+3, strip.Color(intensity,intensity,intensity));
    test_index += 1;
    
    strip.setBrightness(intensity);
    strip.show();
}

