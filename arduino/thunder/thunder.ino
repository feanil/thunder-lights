#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// Center Cloud
#define PIXELS 100
#define CHANCE_OF_MOVING_LOCATION 150
#define CHANCE_OF_BEING_OFF 100


#define PIN 15

Adafruit_NeoPixel strip = Adafruit_NeoPixel(PIXELS, PIN, NEO_GRB + NEO_KHZ800);

uint8_t intensity = 0;
uint8_t test_index = 0;

void setup() {
    Serial.begin(115200);
    strip.begin();
    strip.show();
    randomSeed(40);
}

void loop() {
    if (Serial.available() > 0) {
      intensity = Serial.read();
      pattern_one(intensity);

    } else {
      if(random(CHANCE_OF_MOVING_LOCATION) == 1) {
        pattern_one(0);
      }
      pattern_one(random(100)+100);
      delay(random(50));
    }

    if(random(CHANCE_OF_BEING_OFF) == 1){
      pattern_one(0);
      delay(random(4000)+1000);
    }
}

void pattern_one(uint8_t intensity) {
    if(intensity == 0){
      test_index = random(PIXELS-3)+3;
    }
    
    strip.setPixelColor(test_index-3, strip.Color(0,0,0));
    strip.setPixelColor(test_index-2, strip.Color(64,64,64));
    strip.setPixelColor(test_index-1, strip.Color(128,128,128));
    strip.setPixelColor(test_index, strip.Color(intensity,intensity,intensity));
    strip.setPixelColor(test_index+1, strip.Color(intensity,intensity,intensity));
//    strip.setPixelColor(test_index+2, strip.Color(intensity,intensity,intensity));
//    strip.setPixelColor(test_index+3, strip.Color(intensity,intensity,intensity));
    test_index += 1;
    test_index = test_index % PIXELS;
    
    strip.setBrightness(intensity);
    strip.show();
}

