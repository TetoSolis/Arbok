#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WebServer.h>
#include <WiFiClient.h>

#define SSID "Arbok"
#define PASSWORD "Solgaleo"
#define KEYCLOAK_URL "http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token"
#define INTROSPECT_URL "http://192.168.1.2:8080/realms/Abo/protocol/openid-connect/token/introspect"
#define CLIENT_ID "abra"
#define CLIENT_SECRET "lwGDExe8qiiKGDfM3FFA7hTmfA7W7qUU"
#define SCOPE "psyko"

WebServer server(80);

bool validateToken(const String &token) {
    Serial.println("Validating token...");

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

        if (active) {
            Serial.println("Token is active.");
        } else {
            Serial.println("Token is inactive.");
        }

        return active;
    }
    http.end();
    Serial.println("Failed to validate token. HTTP error code: " + String(httpCode));
    return false;
}

void handleRoot() {
    Serial.println("Handling root request...");

    if (!server.hasHeader("Authorization")) {
        Serial.println("No Authorization header found.");
        server.send(401, "text/plain", "Unauthorized");
        return;
    } else {
        Serial.println("Authorization header found.");
    }

    String authHeader = server.header("Authorization");
    if (!authHeader.startsWith("Bearer ")) {
        Serial.println("Invalid Authorization Header format.");
        server.send(401, "text/plain", "Invalid Authorization Header");
        return;
    } else {
        Serial.println("Valid Authorization Header format.");
    }

    String token = authHeader.substring(7);
    Serial.print("Received Token: ");
    Serial.println(token);  // Output the token for debugging

    if (validateToken(token)) {
        Serial.println("Token is valid.");
        server.send(200, "text/plain", "1");
    } else {
        Serial.println("Invalid Token.");
        server.send(403, "text/plain", "Forbidden");
    }
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(SSID, PASSWORD);
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 30) {  // Limit the number of attempts
        delay(1000);
        Serial.println("Connecting to WiFi...");
        attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("Connected to WiFi");
        Serial.print("IP Address: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println("Failed to connect to WiFi");
    }

    server.on("/", HTTP_GET, handleRoot);
    server.begin();
    Serial.println("Server started.");
}

void loop() {
    server.handleClient();
}

