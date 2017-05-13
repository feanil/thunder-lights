#include <Adafruit_NeoPixel.h>

#define NUM_LEDS 300
#define PIN 7
#define WHITE 255,255,255

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

int lighting_style = 0;
int intensity = 0;
uint8_t index = 0;

void setup() {
    Serial.begin(9600);
    strip.begin();
    strip.show();
}

void loop() {
    if (Serial.available() > 1) {
      lighting_style = Serial.read();
      intensity = Serial.read();

      if(index=0){
        index = random(NUM_LEDS);
      }

      strip.setPixelColor(index, strip.Color(WHITE));
      strip.setBrightness(intensity);
      strip.show();

      
      Serial.print("Index: ");
      Serial.print(index);
      Serial.print("  Intensity:");
      Serial.println(intensity);

      
    }
}
