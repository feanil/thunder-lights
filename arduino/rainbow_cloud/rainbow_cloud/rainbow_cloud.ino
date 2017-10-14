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

void setup() {
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
  #if defined (__AVR_ATtiny85__)
    if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  // End of trinket special code


  strip.begin();
  strip.clear();
  strip.show(); // Initialize all pixels to 'off'
}

void loop() {
  strip.clear();
//  strip.setBrightness(10);
//  rainbow(20);
  rainbowCycle(30);
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j, k;

  uint8_t twinkles [2][4];
  
  twinkles[0][0] = random(0,NUM_PIXELS - 3);
  twinkles[0][1] = twinkles[0][0] + 2;
  twinkles[0][2] = 1;
  twinkles[0][3] = 0;

   twinkles[1][0] = random(0,NUM_PIXELS - 3);
  twinkles[1][1] = twinkles[0][0] + 2;
  twinkles[1][2] = 1;
  twinkles[1][3] = 0;

  for(j=0; j<256; j++) {
    for(k=0; k<1; k++){
      for(i=0; i< strip.numPixels(); i++) {
        if(i < twinkles[k][0] || i > twinkles[k][1]){
          strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
        } else {
        }
      }

      
      for(i=twinkles[k][0]; i<= twinkles[k][1]; i++){
          twinkles[k][3] = twinkles[k][3] + twinkles[k][2];
  
          if(twinkles[k][3] >= 255){
            twinkles[k][3] = 255;
            twinkles[k][2] = twinkles[k][2] * -1;
          }
  
          if(twinkles[k][3] <= 0){
            twinkles[k][3] = 0;
            twinkles[k][2] = twinkles[k][2] * -1;
          }
          strip.setPixelColor(i, strip.Color(twinkles[k][3],twinkles[k][3], twinkles[k][3]));
      }
    }
    strip.show();
    delay(wait);
  }
}

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
