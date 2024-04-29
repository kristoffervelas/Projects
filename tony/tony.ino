
//#include <HCSR04.h> //ultrasonic sensor
//#include <Dht_nonblocking.h>

#include <LiquidCrystal.h>
LiquidCrystal lcd(8, 9, 10, 11, 12, 13);


int dht = 4;
//DHT_nonblocking dht_sensor(dht, DHT_SENSOR_TYPE);
int buzzer = 7;//the pin of the active buzzer
int ledPin = 5;
int enterButton = 6;
int leftButton = 2;
int rightButton = 3;
int morseButton = 22;
int dash = 700;
int dot = 300;
String myString;
String letters[] = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"};
String morse[] = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".--    -", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..    -", "...-", ".--", "-..-", "-.--", "--.."};
//UltraSonicDistanceSensor distanceSensor(13,12);

String lettersDisplay[] = {"_", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"};
uint8_t enterPrev;
uint8_t leftPrev;
uint8_t rightPrev;
void setup()
{
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.clear();
  lcd.print(myString);
  pinMode(buzzer,OUTPUT);//initialize the buzzer pin as an output
  pinMode(ledPin, OUTPUT);//initialize led pin as output
  digitalWrite(ledPin, LOW);//set led to be off initially
  pinMode(enterButton, INPUT_PULLUP);
  pinMode(leftButton, INPUT_PULLUP);
  pinMode(rightButton, INPUT_PULLUP);
  pinMode(morseButton, INPUT_PULLUP);

  //getting the "edge signal" of the buttons
  enterPrev = digitalRead(enterButton);
  leftPrev = digitalRead(leftButton);
  rightPrev = digitalRead(rightButton);


}



int cursorInd = 3;
int letterLeft = 0;
int letterRight = 16;

void loop()
{
  String full = "";
  String cursor = "^";
  unsigned char i;
  //lcd.print(millis() / 1000);

  //print letters, top row
  //have to concatenate the list because doesnt list splice
  lcd.setCursor(0,0);
  for(int i = letterLeft; i < letterRight; i++){
    full += lettersDisplay[i];
  }
  lcd.print(full);


  //The String
  if(enterPrev == HIGH && digitalRead(enterButton) == LOW){
    myString += full[cursorInd];
  }
  enterPrev = digitalRead(enterButton);
  
  //cursor, bottom row
  lcd.setCursor(cursorInd, 1);
  lcd.print(cursor);
  //16 chars
  
  //manipulate the cursor
  if(rightPrev == HIGH && digitalRead(rightButton) == LOW){
    lcd.setCursor(cursorInd, 1);
    lcd.print(" ");
    if(cursorInd == 15){
      letterLeft += 1;
      letterRight += 1;
    }else{
      cursorInd += 1;
    }
  }
  rightPrev = digitalRead(rightButton);


  if(leftPrev == HIGH && digitalRead(leftButton) == LOW){
    lcd.setCursor(cursorInd, 1);
    lcd.print(" ");
    if(cursorInd == 0){
      letterLeft -= 1;
      letterRight -= 1;
    }else{
      cursorInd -= 1;
    }
  }
  leftPrev = digitalRead(leftButton);



  //TO RUN MORSE, ALL THREE BUTTONS HAVE TO BE PRESSED
  if(digitalRead(morseButton) == LOW){
    runMorse();
  }

  //TO CLEAR THE TEXT INPUT
  if(digitalRead(leftButton) == LOW && digitalRead(rightButton) == LOW){
    myString = "";
  }

  /* OG MORSE CODE
  lcd.print("Press the button");

  lcd.setCursor(0,0);
  lcd.print(myString);

  lcd.setCursor(0,1);

  int strLen = myString.length();
  for(int m = 0; m < (strLen + 16); m++){
    lcd.scrollDisplayLeft();
    delay(350);
    if(digitalRead(buttonPin) == LOW){
      runMorse();
    }
  }
  */

  /*
  if(digitalRead(buttonPin) == LOW){
    digitalWrite(ledPin, HIGH);
    
    for(i=0;i<3;i++){
      digitalWrite(buzzer,HIGH);
      delay(1);//wait for 1ms
      digitalWrite(buzzer,LOW);
      delay(1);//wait for 1ms
    }

  }
  else{
    digitalWrite(ledPin, LOW);
  }
  lcd.setCursor(-(strLen+16), 0);
  */


} 

void runMorse(){
  lcd.clear();

  for(int i=0; i < myString.length(); i++){
      
    lcd.setCursor(0, 0); //top left
    int theIndex = getIndex(myString[i]);
    String code = morse[theIndex];
    lcd.print(myString[i]); //print current letter being coded

    lcd.setCursor(0, 1); //bottom left
    for(int m = 0; m < code.length(); m++){
      if(code[m] == '-'){
        dashOut();
        lcd.print("-");
      }
      if(code[m] == '.'){
        dotOut();
        lcd.print(".");
      }
      if(code[m] == ' '){
        spaceOut();
        lcd.print(" ");
      }
        
      delay(500);
    }
    lcd.clear();
    delay(500);
    digitalWrite(buzzer, HIGH);
    delay(50);
    digitalWrite(buzzer, LOW);
    delay(50);
    digitalWrite(buzzer, HIGH);
    delay(50);
    digitalWrite(buzzer, LOW);
    delay(500);
  }
}

int getIndex(char letter){
  int counter = 0;
  int result = 50;
  for(int j = 0; j < sizeof(letters); j++){
    if (String(letter) == letters[j]){
      result = counter;
      break;
    }
    counter += 1;
  }
  return result;
}

void spaceOut(){
  delay(700);
}

void dashOut(){
  digitalWrite(buzzer, HIGH);
  digitalWrite(ledPin, HIGH);
  delay(dash);
  digitalWrite(buzzer, LOW);
  digitalWrite(ledPin, LOW);
}

void dotOut(){
  digitalWrite(buzzer, HIGH);
  digitalWrite(ledPin, HIGH);
  delay(dot);
  digitalWrite(buzzer, LOW);
  digitalWrite(ledPin, LOW);
}






/*
    //output an frequency
    for(i=0;i<80;i++){
      digitalWrite(buzzer,HIGH);
      delay(1);//wait for 1ms
      digitalWrite(buzzer,LOW);
      delay(1);//wait for 1ms
    }
    //output another frequency
    for(i=0;i<100;i++){
      digitalWrite(buzzer,HIGH);
      delay(2);//wait for 2ms
      digitalWrite(buzzer,LOW);
      delay(2);//wait for 2ms
    }
    */


















/*
if (irrecv.decode(&results)) // have we received an IR signal?

  {
    Serial.println(results.value, HEX);
    switch(results.value)

    {

      case 0xFFA857: // VOL+ button pressed
                      small_stepper.setSpeed(500); //Max seems to be 500
                      Steps2Take  =  2048;  // Rotate CW
                      small_stepper.step(Steps2Take);
                      delay(2000); 
                      break;

      case 0xFF629D: // VOL- button pressed
                      small_stepper.setSpeed(500);
                      Steps2Take  =  -2048;  // Rotate CCW
                      small_stepper.step(Steps2Take);
                      delay(2000); 
                      break;
                
    }
    
      irrecv.resume(); // receive the next value
                 digitalWrite(8, LOW);
                 digitalWrite(9, LOW);
                 digitalWrite(10, LOW);
                 digitalWrite(11, LOW);       
  }  
*/




/* --end main loop -- */

/*
#include <Servo.h>

Servo myservo;
int ledPin = 5;
int buttonAPin = 6;
int buttonBPin = 7;
int pos = 0;

void setup() {
  
  Serial.begin(9600);
  myservo.attach(9);
  myservo.write(90);
  pinMode(ledPin, OUTPUT);
  pinMode(buttonAPin, INPUT_PULLUP);
  pinMode(buttonBPin, INPUT_PULLUP);
}

  if(digitalRead(buttonAPin) == LOW){
      digitalWrite(ledPin, HIGH);
      pos += 1;
      myservo.write(pos);
  }

  if(digitalRead(buttonBPin) == LOW){
      digitalWrite(ledPin, HIGH);
      pos -= 1;
      myservo.write(pos);
  }
 
}
*/




//FOR SERVO ONLY 180 Deg
/*
if(digitalRead(buttonAPin) == LOW){
      digitalWrite(ledPin, HIGH);
      pos += 1;
      myservo.write(pos);
      if(pos > 180){
        pos = 180;
      }
  }

  if(digitalRead(buttonBPin) == LOW){
      digitalWrite(ledPin, HIGH);
      pos -= 1;
      myservo.write(pos);
      if(pos < 5){
        pos = 5;
      }
  }
*/

/*
#include <Servo.h>

Servo myservo;

int pos = 0;

void setup() {
  Serial.begin(9600);
  myservo.attach(9);
}
void loop() {
  myservo.write(90);
  delay(1000);
  myservo.write(60);
  delay(1000);
  myservo.write(90);
  delay(1000);
  myservo.write(160);
  delay(1000);
 
}
*/



/*
int ledPin = 5;
int buttonApin = 9;
int buttonBpin = 8;
void setup() {
  // put your setup code here, to run once:
  pinMode(ledPin, OUTPUT);
  pinMode(buttonApin, INPUT_PULLUP);
  pinMode(buttonBpin, INPUT_PULLUP);


}

void loop() {
  bool activate = true;
  // put your main code here, to run repeatedly:
  if(digitalRead(buttonApin) == LOW){
    digitalWrite(ledPin, HIGH);
    //delay(100);
    //digitalWrite(ledPin, LOW);
    //delay(100);
  }
  if(digitalRead(buttonBpin) == LOW){
    activate = false;
    digitalWrite(ledPin, LOW);
  }
}
*/