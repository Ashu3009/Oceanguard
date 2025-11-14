#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// ⬇️ YOUR WIFI DETAILS
const char* ssid = "The Student Scoop";
const char* password = "TSS@2023";

// ⬇️ Your server endpoint
String serverURL = "http://192.168.0.177:8000/upload-image/";

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
  Serial.println("🌊 OceanGuard - MAXIMUM QUALITY MODE");

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
    Serial.println("\n❌ WiFi FAILED!");
    while(1) { delay(1000); }
  }

  Serial.println("\n✅ WiFi Connected!");
  Serial.print("📡 IP: ");
  Serial.println(WiFi.localIP());

  // ============================================
  // 🏆 MAXIMUM QUALITY CONFIGURATION
  // ============================================
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

  // 🏆 MAXIMUM SETTINGS
  config.frame_size = FRAMESIZE_UXGA;  // 1600x1200 (MAXIMUM!)
  config.jpeg_quality = 6;             // 6 = Best quality (1-63, lower=better)
  config.fb_count = 2;                 // Double buffering
  config.grab_mode = CAMERA_GRAB_LATEST; // Always grab latest frame

  Serial.println("📷 Initializing MAXIMUM QUALITY camera...");
  esp_err_t err = esp_camera_init(&config);

  if (err != ESP_OK) {
    Serial.printf("❌ Camera Init FAILED: 0x%x\n", err);
    // Try fallback to SVGA if UXGA fails
    Serial.println("⚠️ UXGA failed, trying SVGA fallback...");
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 8;
    err = esp_camera_init(&config);

    if (err != ESP_OK) {
      Serial.println("❌ Camera completely failed!");
      while(1) { delay(1000); }
    }
  }

  Serial.println("✅ Camera Ready!");

  // 🏆 MAXIMUM IMAGE ENHANCEMENTS
  sensor_t * s = esp_camera_sensor_get();
  if (s != NULL) {
    s->set_brightness(s, 0);     // 0 = neutral
    s->set_contrast(s, 2);       // +2 = max contrast (sharper edges)
    s->set_saturation(s, 0);     // 0 = neutral
    s->set_sharpness(s, 2);      // +2 = maximum sharpness
    s->set_denoise(s, 0);        // Disable noise reduction (keeps detail)
    s->set_special_effect(s, 0); // No effects
    s->set_whitebal(s, 1);       // Auto white balance ON
    s->set_awb_gain(s, 1);       // Auto white balance gain ON
    s->set_wb_mode(s, 0);        // Auto WB mode
    s->set_exposure_ctrl(s, 1);  // Auto exposure ON
    s->set_aec2(s, 1);           // Auto exposure algorithm ON
    s->set_ae_level(s, 0);       // Exposure level 0
    s->set_aec_value(s, 400);    // Higher = brighter (300-600 good range)
    s->set_gain_ctrl(s, 1);      // Auto gain ON
    s->set_agc_gain(s, 0);       // Auto gain ceiling (0 = auto)
    s->set_gainceiling(s, (gainceiling_t)0); // Auto ceiling
    s->set_bpc(s, 1);            // Black pixel correction ON
    s->set_wpc(s, 1);            // White pixel correction ON
    s->set_raw_gma(s, 1);        // Gamma correction ON
    s->set_lenc(s, 1);           // Lens correction ON
    s->set_hmirror(s, 0);        // Horizontal mirror OFF
    s->set_vflip(s, 0);          // Vertical flip OFF
    s->set_dcw(s, 0);            // Downscale OFF (keep max resolution)
    s->set_colorbar(s, 0);       // Test pattern OFF

    Serial.println("✅ MAXIMUM quality settings applied!");
  }

  // Test capture
  Serial.println("🧪 Testing...");
  camera_fb_t * test_fb = esp_camera_fb_get();
  if (!test_fb) {
    Serial.println("❌ Test FAILED!");
    while(1) { delay(1000); }
  } else {
    Serial.printf("✅ Test OK! Size: %d bytes (MAXIMUM QUALITY)\n", test_fb->len);
    Serial.printf("   Resolution: %dx%d\n", test_fb->width, test_fb->height);
    esp_camera_fb_return(test_fb);
  }

  Serial.println("\n🚀 MAXIMUM QUALITY MODE ACTIVE!\n");
  delay(2000);
}

int capture_count = 0;

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("❌ WiFi Lost! Reconnecting...");
    WiFi.reconnect();
    delay(5000);
    return;
  }

  Serial.printf("\n📸 Capture #%d - MAXIMUM QUALITY...\n", ++capture_count);

  // Flash ON for 200ms (better lighting)
  digitalWrite(LED_PIN, HIGH);
  delay(200);

  camera_fb_t * fb = esp_camera_fb_get();

  if (!fb) {
    Serial.println("❌ Capture FAILED!");
    digitalWrite(LED_PIN, LOW);
    delay(2000);
    return;
  }

  Serial.printf("✅ Captured! Size: %d bytes (%dx%d)\n", fb->len, fb->width, fb->height);

  // Upload
  Serial.println("📤 Uploading...");
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "image/jpeg");
  http.setTimeout(20000); // 20 sec timeout (large files)

  int httpResponseCode = http.POST(fb->buf, fb->len);

  if (httpResponseCode > 0) {
    Serial.printf("✅ SUCCESS! Response: %d\n", httpResponseCode);
    String response = http.getString();
    Serial.println("Server: " + response);
  } else {
    Serial.printf("❌ FAILED! Error: %s\n", http.errorToString(httpResponseCode).c_str());
  }

  http.end();
  esp_camera_fb_return(fb);
  digitalWrite(LED_PIN, LOW);

  Serial.println("⏳ Waiting 8 seconds...");
  delay(8000);
}
