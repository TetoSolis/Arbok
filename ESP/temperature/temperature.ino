#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 21  // GPIO12 (D6)

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
    Serial.begin(115200);
    while (!Serial);
    Serial.println("Lecture de la température DS18B20...");
    sensors.begin();
}

void loop() {
    sensors.requestTemperatures();  
    float temp = sensors.getTempCByIndex(0);

    if (temp == -127.0) {
        Serial.println("Erreur : Capteur non détecté !");
    } else {
        Serial.print("Température : ");
        Serial.print(temp);
        Serial.println(" °C");
    }
    delay(1000);
}
