//Sample using LiquidCrystal library
#include <LiquidCrystal.h>

/*******************************************************

This program will test the LCD panel and the buttons
Mark Bramwell, July 2010

********************************************************/

// select the pins used on the LCD panel
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

// define some values used by the panel and buttons
int lcd_key     = 0;
int adc_key_in  = 0;
#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   5

// read the buttons
int read_LCD_buttons()
{
 adc_key_in = analogRead(0);      // read the value from the sensor
 // my buttons when read are centered at these valies: 0, 144, 329, 504, 741
 // we add approx 50 to those values and check to see if we are close
 if (adc_key_in > 1000) return btnNONE; // We make this the 1st option for speed reasons since it will be the most likely result
 // For V1.1 us this threshold
 if (adc_key_in < 50)   return btnRIGHT;
 if (adc_key_in < 250)  return btnUP;
 if (adc_key_in < 450)  return btnDOWN;
 if (adc_key_in < 650)  return btnLEFT;
 if (adc_key_in < 850)  return btnSELECT;

 // For V1.0 comment the other threshold and use the one below:
/*
 if (adc_key_in < 50)   return btnRIGHT;
 if (adc_key_in < 195)  return btnUP;
 if (adc_key_in < 380)  return btnDOWN;
 if (adc_key_in < 555)  return btnLEFT;
 if (adc_key_in < 790)  return btnSELECT;
*/


 return btnNONE;  // when all others fail, return this...
}
String serial_input;
void setup()
{
 lcd.begin(16, 2);              // start the library
 Serial.begin(9600);
   delay(2000);
   while (!Serial.available()){
    // display each character to the LCD
    delay(3000L);         // Sleep for 3 seconds
    lcd.setCursor(0, 0);
    lcd.print("  Bitcoin Cash");
    lcd.setCursor(0, 1);
    lcd.print("  Coin Machine");
    delay(3000L);         // Sleep for 3 seconds
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("  Text BEGIN @");
    lcd.setCursor(0, 1);
    lcd.print("  226-401-8327");
  }
}

void loop()
{
  if(Serial.available()){
      serial_input = Serial.readStringUntil('\n');
      lcd.clear();
      lcd.print(serial_input);
  }
} 
