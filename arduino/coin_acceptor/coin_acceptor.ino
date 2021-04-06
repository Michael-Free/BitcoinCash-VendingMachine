volatile byte coinPulseCount=0;    // a counter to see how many times the pin has changed - which coin inserted
byte newCoinInserted; // a place to put our last coin pulse count
byte cmd=0;     // a place to put our serial data
int opCountPin = 3;  // pin3 as optical count input
volatile unsigned long pulseTime;  //this stores the time of the last pulse.

void setup() {
  Serial.begin(9600);
  Serial.println("Initialized...");
  pinMode(opCountPin, INPUT);     //optical count is an input
  attachInterrupt(1, coinpulse, RISING); // attach a PinChange Interrupt to our pin on the rising edge
  }

void loop()
{
  //SERIAL MONITOR STUFF
  cmd=Serial.read(); 
  if (cmd=='p')
  {
    Serial.print("coinPulseCount:\t");
    Serial.println(coinPulseCount, DEC);
  }
  cmd=0;

//CHECK NOW TO SEE WHICH COIN IS INSERTED

if (coinPulseCount >0 && millis()- pulseTime > 1000)    //if there is a coin count & the time between now and the last pulse is greater than 1/4 of a second - THE END OF BANK OF PULSES
  {
    newCoinInserted = coinPulseCount;  //new variable to free up coinPulseCount on the interrupt.
    coinPulseCount = 0;                // clear pulse count ready for a new pulse on the interrupt.
  }

//Proccess the coin inserted

switch (newCoinInserted) {
  case 3:   
    Serial.println("2");
    newCoinInserted = 0;   
    break;
  case 6:   
    Serial.println("1");
    newCoinInserted = 0;   
    break;
  case 9:   
    Serial.println("0.25");
    newCoinInserted = 0;   
    break;
  case 12:   
    Serial.println("0.10");
    newCoinInserted = 0;   
    break;
 
  }
}

void coinpulse()
{
  coinPulseCount++;
  pulseTime = millis();   //store current time in pulseTime
}
