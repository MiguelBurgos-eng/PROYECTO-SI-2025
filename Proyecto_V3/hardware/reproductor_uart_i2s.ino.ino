#include <driver/i2s.h>

#define I2S_NUM         I2S_NUM_0
#define I2S_BCLK        26
#define I2S_LRC         25
#define I2S_DOUT        22

#define AUDIO_BUFFER    512  // Tamaño del buffer de audio

void setupI2S() {
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
    .sample_rate = 44100,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S_MSB,
    .intr_alloc_flags = 0,
    .dma_buf_count = 8,
    .dma_buf_len = 64,
    .use_apll = false,
    .tx_desc_auto_clear = true,
    .fixed_mclk = 0
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_BCLK,
    .ws_io_num = I2S_LRC,
    .data_out_num = I2S_DOUT,
    .data_in_num = I2S_PIN_NO_CHANGE
  };

  i2s_driver_install(I2S_NUM, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM, &pin_config);
  i2s_zero_dma_buffer(I2S_NUM);
}

void setup() {
  setupI2S();
  Serial.begin(921600);
  while (!Serial);
  Serial.println("🎧 Esperando audio...");
}

void loop() {
  static bool reproduciendo = false;
  static char comando[16] = {0};  // Para __START__ o __END__
  static uint8_t buffer[AUDIO_BUFFER];
  static size_t len = 0;

  while (Serial.available()) {
    if (!reproduciendo) {
      char c = Serial.read();
      if (len < sizeof(comando) - 1) {
        comando[len++] = c;
      }

      if (c == '\n') {
        comando[len] = '\0';
        if (strstr(comando, "__START__")) {
          Serial.println("▶️ Reproduciendo...");
          reproduciendo = true;
        }
        len = 0;
      }
    } else {
      int bytesRead = Serial.readBytes(buffer, AUDIO_BUFFER);
      if (bytesRead == 9 && memcmp(buffer, "__END__\n", 9) == 0) {
        Serial.println("⏹️ Fin de audio.");
        reproduciendo = false;
      } else if (bytesRead > 0) {
        Serial.print(".");  // Confirmación de que está recibiendo audio
        size_t bytesWritten;
        i2s_write(I2S_NUM, buffer, bytesRead, &bytesWritten, portMAX_DELAY);
      }
    }
  }
}
