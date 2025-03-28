#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define IR_SENSOR 3

DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(9600);
    Serial.println("Arduino Sensor Monitoring Started...");
    dht.begin();
    pinMode(IR_SENSOR, INPUT);
}

void loop() {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int motion = digitalRead(IR_SENSOR);

    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("DHT Sensor Error!");
    } else {
        Serial.print(temperature);
        Serial.print(",");
        Serial.print(humidity);
        Serial.print(",");
        Serial.println(motion);
    }
    delay(200);
}
