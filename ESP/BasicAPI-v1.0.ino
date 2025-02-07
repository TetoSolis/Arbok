#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WebServer.h>

#define SSID "Arbok"
#define PASSWORD "Solgaleo"
#define KEYCLOAK_URL "http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token"
#define INTROSPECT_URL "http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token/introspect"
#define CLIENT_ID "abra"
#define CLIENT_SECRET "lwGDExe8qiiKGDfM3FFA7hTmfA7W7qUU"
#define SCOPE "psyko"

WebServer server(80);

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
        server.send(200, "text/plain", "1");
    } else {
        server.send(403, "text/plain", "Forbidden");
    }
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(SSID, PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    server.on("/", HTTP_GET, handleRoot);
    server.begin();
}

void loop() {
    server.handleClient();
}
