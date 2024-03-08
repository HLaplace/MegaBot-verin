const int pinLed1 = 13;
const int pinLed2 = 27;
const int pinLed3 = 33;

void setup() {
  Serial.begin(115200);
  pinMode(pinLed1, OUTPUT);
  pinMode(pinLed2, OUTPUT);
  pinMode(pinLed3, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    
    String input = Serial.readStringUntil('\n');
    if (input == "L11") {
      Serial.print("Verin 1 : ");
      toggleLed(pinLed1);
      
    } else if (input == "L12") {
      Serial.print("Verin 2 : ");
      toggleLed(pinLed2);
      
    } else if (input == "L13") {
      Serial.print("Verin 3 : ");
      toggleLed(pinLed3);
      
    }  else {
       Serial.println("Aucun verin");
     }
  }
}

void toggleLed(int pin) {
  if (digitalRead(pin) == HIGH) {
    digitalWrite(pin, LOW);
    Serial.println("Extinction");
  } else {
    digitalWrite(pin, HIGH);
    Serial.println("Allumage"); 
  }
}
