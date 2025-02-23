#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WebServer.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define SSID "Arbok"
#define PASSWORD "Solgaleo"
#define KEYCLOAK_URL "http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token"
#define INTROSPECT_URL "http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token/introspect"
#define CLIENT_ID "abra"
#define CLIENT_SECRET "qc3c05GiFknf1io0vAOAsOETpgGdOkSD"
#define SCOPE "psyko"

// Définition de l'IP statique
IPAddress local_IP(192, 168, 1, 5);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

WebServer server(80);

// Capteur de température DS18B20 (OneWire sur GPIO 21)
const int oneWireBus = 21;
OneWire oneWire(oneWireBus);
DallasTemperature sensors(&oneWire);

bool validateToken(const String &token) {
    HTTPClient http;
    http.begin(INTROSPECT_URL);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    String postData = "client_id=" + String(CLIENT_ID) +
                      "&client_secret=" + String(CLIENT_SECRET) +
                      "&token=" + token;

    int httpCode = http.POST(postData);
    if (httpCode == 200) {
        DynamicJsonDocument doc(1024);
        deserializeJson(doc, http.getString());
        bool active = doc["active"];
        http.end();
        return active;
    }
    http.end();
    return false;
}

void handleRoot() {
    // Ajouter les en-têtes CORS
    server.sendHeader("Access-Control-Allow-Origin", "*"); // Autorise toutes les origines
    server.sendHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    server.sendHeader("Access-Control-Allow-Headers", "Authorization, Content-Type");

    if (!server.hasHeader("Authorization")) {
        server.send(401, "text/plain", "Unauthorized");
        return;
    }
    String authHeader = server.header("Authorization");
    if (!authHeader.startsWith("Bearer ")) {
        server.send(401, "text/plain", "Invalid Authorization Header");
        return;
    }
    String token = authHeader.substring(7);
    if (validateToken(token)) {
        // Lecture de la température
        sensors.requestTemperatures();
        float temperature = sensors.getTempCByIndex(0);

        if (temperature == -127.0) {
            server.send(500, "application/json", "{\"error\": \"Erreur de lecture du capteur\"}");
            return;
        }

        // Création d'un JSON avec la température
        DynamicJsonDocument doc(200);
        doc["message"] = "Température récupérée avec succès";
        doc["temperature"] = temperature;

        String responseBody;
        serializeJson(doc, responseBody);

        server.send(200, "application/json", responseBody);
    } else {
        server.send(403, "text/plain", "Forbidden");
    }
}

// Ajout de la gestion des requêtes OPTIONS
void handleOptions() {
    // Répondre aux pré-demande CORS
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.sendHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    server.sendHeader("Access-Control-Allow-Headers", "Authorization, Content-Type");
    server.send(200, "text/plain", "");
}

void setup() {
    Serial.begin(115200);

    // Configuration de l'IP statique
    if (!WiFi.config(local_IP, gateway, subnet)) {
        Serial.println("⚠️ Erreur lors de l'attribution de l'IP statique !");
    }

    // Connexion WiFi
    WiFi.begin(SSID, PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("📡 Connexion au WiFi...");
    }

    Serial.println("✅ WiFi connecté !");
    Serial.print("📡 Adresse IP de l'ESP32 : ");
    Serial.println(WiFi.localIP());

    // Initialisation du capteur de température
    sensors.begin();

    // Définition de la route REST
    server.on("/", HTTP_GET, handleRoot);

    // Définition de la gestion de la requête OPTIONS pour CORS
    server.on("/", HTTP_OPTIONS, handleOptions);

    // Démarrage du serveur
    server.begin();
    Serial.println("🌐 Serveur API REST démarré !");
}

void loop() {
    server.handleClient();  // Gère les requêtes entrantes
}