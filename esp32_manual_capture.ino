#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi Details
const char* ssid = "The Student Scoop";
const char* password = "TSS@2023";

// Server endpoints
String serverURL = "http://192.168.0.177:8000/upload-image/";
String checkCaptureURL = "http://192.168.0.177:8000/check-capture/";

// Camera Module: AI Thinker
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22
#define LED_PIN 33

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("OceanGuard ESP32-CAM - Manual Capture Mode");

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // WiFi Connection
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  int wifi_attempts = 0;
  while (WiFi.status() != WL_CONNECTED && wifi_attempts < 20) {
    Serial.print(".");
    delay(500);
    wifi_attempts++;
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\nWiFi Connection FAILED!");
    while(1) { delay(1000); }
  }

  Serial.println("\nWiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Camera Configuration
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  Serial.println("Initializing camera...");
  esp_err_t err = esp_camera_init(&config);

  if (err != ESP_OK) {
    Serial.printf("Camera Init FAILED: 0x%x\n", err);
    while(1) { delay(1000); }
  }

  Serial.println("Camera Ready!");
  Serial.println("System Ready - Waiting for manual capture requests...\n");
  delay(2000);
}

void captureAndUpload() {
  Serial.println("Taking photo...");
  digitalWrite(LED_PIN, HIGH);

  camera_fb_t * fb = esp_camera_fb_get();

  if (!fb) {
    Serial.println("Camera capture FAILED!");
    digitalWrite(LED_PIN, LOW);
    return;
  }

  Serial.printf("Photo captured! Size: %d bytes\n", fb->len);

  // Upload to Server
  Serial.println("Uploading to server...");
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "image/jpeg");
  http.setTimeout(20000);

  int httpResponseCode = http.POST(fb->buf, fb->len);

  if (httpResponseCode > 0) {
    Serial.printf("Upload SUCCESS! Response: %d\n", httpResponseCode);
    String response = http.getString();
    Serial.println("Server: " + response);
  } else {
    Serial.printf("Upload FAILED! Error: %s\n", http.errorToString(httpResponseCode).c_str());
  }

  http.end();
  esp_camera_fb_return(fb);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  // Check WiFi
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi Disconnected! Reconnecting...");
    WiFi.reconnect();
    delay(5000);
    return;
  }

  // Poll server for manual capture requests
  HTTPClient http;
  http.begin(checkCaptureURL);
  http.setTimeout(5000);

  int httpResponseCode = http.GET();

  if (httpResponseCode > 0) {
    String response = http.getString();

    // Parse JSON response
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, response);

    if (!error) {
      bool shouldCapture = doc["capture"];

      if (shouldCapture) {
        Serial.println("\nMANUAL CAPTURE REQUEST RECEIVED!");
        captureAndUpload();
      } else {
        // No capture request - just waiting
        Serial.print(".");
      }
    }
  }

  http.end();

  // Poll every 2 seconds
  delay(2000);
}
