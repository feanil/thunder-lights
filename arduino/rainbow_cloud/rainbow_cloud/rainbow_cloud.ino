#include <TimedAction.h>

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 7
#define NUM_PIXELS 300
// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, PIN, NEO_GRB + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.



uint8_t twinkles [3][4];
uint16_t first_color;
int counter = 0;

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  uint8_t darkness = 12;
  if(WheelPos < 85) {
    return strip.Color((255 - WheelPos * 3)/darkness, 0, (WheelPos * 3)/darkness);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, (WheelPos * 3)/darkness, (255 - WheelPos * 3)/darkness);
  }
  WheelPos -= 170;
  return strip.Color((WheelPos * 3)/darkness, (255 - WheelPos * 3)/darkness, 0);
}

void updateTwinkle(){
  uint8_t i;
  for(i=twinkles[0][0];i<=(twinkles[0][0] + 2); i++){
    strip.setPixelColor(i, strip.Color(twinkles[0][2],twinkles[0][2],twinkles[0][2]));
  }
  twinkles[0][2] = twinkles[0][2] + twinkles[0][3];
  if(twinkles[0][2] >= 255){
    twinkles[0][2] = 255;
    twinkles[0][3] = twinkles[0][3] * -1;
  }
  
  if(twinkles[0][2] <= 0){
    twinkles[0][2] = 0;
    twinkles[0][3] = twinkles[0][3] * -1;
  }
}

void updateTwinkleLocation(){
  if( random(0,3) == 0){
    twinkles[0][0] = random(0, NUM_PIXELS-3);
  } 
}

void updateRainbow() {
  first_color = (first_color + 1) & 255;
 
  uint16_t i;
  // Update all the lights to be a rainbow starting at this color.
  for(i=0; i< strip.numPixels(); i++) {
    strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + first_color) & 255));
  }
}

void show_strip() {
  strip.show();
}

TimedAction ta_updateTwinkle = TimedAction(10, updateTwinkle);
TimedAction ta_showStrip = TimedAction(1, show_strip);
TimedAction ta_updateRainbow = TimedAction(10, updateRainbow);
TimedAction ta_updateTwinkleLocation = TimedAction(1000, updateTwinkleLocation);


void setup() {

  strip.begin();
  strip.clear();
  strip.show(); // Initialize all pixels to 'off'

  randomSeed(analogRead(0));

  twinkles[0][0] = random(0,NUM_PIXELS - 3);
  twinkles[0][2] = 1;
  twinkles[0][3] = 1;
}


void loop() {
//  strip.setBrightness(10);

  // Setup standard rainbow
  ta_updateRainbow.check();
  ta_updateTwinkle.check();
  ta_updateTwinkleLocation.check();
  strip.show();
}
