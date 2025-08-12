const int pinMicrofono = 34;    // OUT del MAX9814 en GPIO34 (ADC)
const int numMuestras = 24000;  // 3 s a 7500 Hz -> ajustas en Python; aquí iteramos 24000
const int pinBoton = 32;        // Botón a GND, pin con PULLUP

void setup() {
  Serial.begin(115200);                 // <-- igual que BAUDRATE en Python
  pinMode(pinBoton, INPUT_PULLUP);       // botón con pull-up interno
  delay(1000);
  Serial.println("ESP32 listo para capturar audio.");
}

void loop() {
  // 1) Si presionas el botón, avisa al PC con 'G' (como "F5")
  static int last = HIGH;
  int now = digitalRead(pinBoton);
  if (last == HIGH && now == LOW) {      // flanco de bajada
    delay(20);                           // debounce sencillo
    if (digitalRead(pinBoton) == LOW) {
      Serial.write('G');                 // notifica al Python
      // opcional: espera a que sueltes para no spamear
      while (digitalRead(pinBoton) == LOW) { delay(5); }
    }
  }
  last = now;

  // 2) Mantengo tu protocolo: cuando llegue 'G' desde el PC, graba y envía
  if (Serial.available()) {
    char comando = Serial.read();
    if (comando == 'G') {  // Iniciar captura
      for (int i = 0; i < numMuestras; i++) {
        uint16_t valor16 = analogRead(pinMicrofono);  // 0..4095
        // Little endian: primero byte bajo, luego byte alto
        Serial.write((uint8_t)(valor16 & 0xFF));
        Serial.write((uint8_t)(valor16 >> 8));
        delayMicroseconds(133); // ~7500 Hz (ajusta fino si lo deseas)
      }
      // sin println para no meter bytes extra en la lectura fija
    }
  }
}
