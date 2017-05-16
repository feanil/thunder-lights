#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define NUM_LEDS 300
#define PIN 7

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

uint8_t intensity = 0;
uint8_t index = 0;

void setup() {
    Serial.begin(9600);
    strip.begin();
    strip.show();
    randomSeed(analogRead(0));
}

void loop() {
    if (Serial.available() > 0) {
      intensity = Serial.read();

      if(intensity == 0){
        index = random(294)+3;
      }

    
      strip.setPixelColor(index, strip.Color(255,255,255));
      strip.setPixelColor(index+1, strip.Color(255,255,255));
      strip.setPixelColor(index+2, strip.Color(255,255,255));
      strip.setPixelColor(index+3, strip.Color(255,255,255));
      index -= 1;


      strip.setBrightness(intensity);
      strip.show();
//      Serial.println(index);
    }
}
