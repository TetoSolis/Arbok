#include <OneWire.h>
#include <DallasTemperature.h>

float temp = 0.0;
const int oneWireBus = 21;  
const int ledPin = 2;  

OneWire oneWire(oneWireBus);
DallasTemperature sensors(&oneWire);

void setup() {
  pinMode(ledPin, OUTPUT);  
  digitalWrite(ledPin, LOW);  /

  Serial.begin(115200);
  Serial.println("Bas on Tech - 1-wire temperature sensor");

  sensors.begin();
}

void loop() {
  sensors.requestTemperatures();
  temp = sensors.getTempCByIndex(0);

  if (temp == -127.0) {
    Serial.println("Erreur : Impossible de lire le capteur !");
  } else {
    Serial.print("Temperature is: ");
    Serial.println(temp);
  }

  // Allume la LED (juste pour la démonstration)
  digitalWrite(ledPin, HIGH);
  delay(1000);
  digitalWrite(ledPin, LOW);
  delay(1000);
}
