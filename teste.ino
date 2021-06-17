#include <SPI.h>
#include <MFRC522.h>

// INPUT
#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN);

// Init array that will store new NUID
byte nuidPICC[4];

void setup() {
  Serial.begin(9600);
  SPI.begin();      // Init SPI bus
  rfid.PCD_Init();  // Init MFRC522

  Serial.println(F("Scan RFID NUID..."));
}

void loop() {
  readRFID();
  delay(200);
}

//
void readRFID() {
  if (!rfid.PICC_IsNewCardPresent())
    return;

  if (!rfid.PICC_ReadCardSerial())
    return;

  if (rfid.uid.uidByte[0] != nuidPICC[0] || rfid.uid.uidByte[1] != nuidPICC[1] || rfid.uid.uidByte[2] != nuidPICC[2] || rfid.uid.uidByte[3] != nuidPICC[3]) {
    String rfid = "";
    for (byte i = 0; i < 4; i++) {
      nuidPICC[i] = rfid.uid.uidByte[i];
      rfid += nuidPICC[i];
    }
    // send rfid data to serial and to be getby python
    Serial.println(rfid);

  }
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}