#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <OneWire.h>
#include <DallasTemperature.h>

const char* ssid = "Arbok";       // Remplace par ton réseau WiFi
const char* password = "Solgaleo"; // Remplace par ton mot de passe

WebServer server(80);  // Création du serveur web sur le port 80

// Token Bearer attendu
const String expectedToken = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJZYklaaDhOVF9SbGs5ZnFGZGFqVEtRXzBYSjdYbXV1WFhNeTZtWWw4SmlZIn0.eyJleHAiOjE3Mzg4NDg5NzUsImlhdCI6MTczODg0ODY3NSwianRpIjoiMzNmNGZmYjktYjU4OS00MTFiLWIwZTktNDczMmJiYzJmNTNjIiwiaXNzIjoiaHR0cDovLzE5Mi4xNjguMS4yOjgwODAvcmVhbG1zL0VzcF9BcGkiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiNDI5YWE0NDEtNGE0Yi00YzMwLThjZjYtNGQ1M2VlOTk5NWI0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZXNwLWNsaWVudCIsInNpZCI6IjMyNDI3YmM1LTc1NmYtNDRhMC04NWNkLWY2NmZlNTJlNmZlYSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cDovLzE5Mi4xNjguMS4xMzciXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1lc3BfYXBpIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6InRoZW8gbWFyY2hhbmQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJlc3AtdXNlciIsImdpdmVuX25hbWUiOiJ0aGVvIiwiZmFtaWx5X25hbWUiOiJtYXJjaGFuZCIsImVtYWlsIjoidGhlby5tYXJjaGFuZDA5MTRAZ21haWwuY29tIn0.HEjW2bH8a8KLPGDIS4t6CbWI5cdvHAV1V8EpNiZU30bAEdZ93yngxKsfD_2LlnS2HihWsukoFkcN3PgjvfZFnyQXZBPqLwHUWLDB2gSD1qxgXzlwpCvh3GD9lcgFPsasmQw406oT-Ft9Ywy4l1IIz7pQXaKqhKJ-6vJCxbEKqe1f3k6xPwU-RFh7oK6e84wDHJEehOOePY24Ame3lKUK-uwT1pNrm49X1OvTjlscst0UwdnS20NKowfThXLEtPCAg8_Aoo3ca4iMwc71q922ci6BUr9tViOb16UU7ImDAwvY6uCIEoKjZcPPXV_9MUMuIl5_kb_LnGg90rH4oHD0HA"; 

// Initialisation du capteur de température
float temp = 0.0;
const int oneWireBus = 21;  // Pin pour le bus 1-wire
OneWire oneWire(oneWireBus);
DallasTemperature sensors(&oneWire);

// Route principale - Affiche la température
void handleTemperature() {
    // Vérifie si le token Bearer est correct
    if (server.header("Authorization") != "Bearer " + expectedToken) {
        server.send(401, "application/json", "{\"error\": \"Unauthorized\"}");
        return;
    }

    // Lecture de la température
    sensors.requestTemperatures();
    temp = sensors.getTempCByIndex(0);

    if (temp == -127.0) {
        server.send(500, "application/json", "{\"error\": \"Erreur de lecture du capteur\"}");
        return;
    }

    // Création d'un JSON avec la température
    StaticJsonDocument<200> doc;
    doc["message"] = "Température récupérée avec succès";
    doc["temperature"] = temp;

    String responseBody;
    serializeJson(doc, responseBody);

    server.send(200, "application/json", responseBody);
}

void setup() {
    Serial.begin(115200);

    // Connexion WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connecté !");
    Serial.print("Adresse IP de l'ESP32 : ");
    Serial.println(WiFi.localIP());

    // Initialisation du capteur de température
    sensors.begin();

    // Définition de la route REST
    server.on("/", HTTP_GET, handleTemperature);

    // Démarrage du serveur
    server.begin();
    Serial.println("Serveur API REST démarré !");
}

void loop() {
    server.handleClient();  // Gère les requêtes entrantes
}
