// We used a 16X2 LCD to display state changes, an RFID tag reader to enable and disable the alarm and a relay to turn a light on

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
const int relay = 53;
char junk;
String inputString="";
String distance_cm = "500";

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  lcd.print("Klaar om te");
  lcd.setCursor(0,2);
  lcd.print("verbinden!");
  Serial.begin(9600);
  pinMode(relay, OUTPUT);
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop()
{
  if(Serial.available()){
  while(Serial.available())
    {
      char inChar = (char)Serial.read(); //read the input
      inputString += inChar;        //make a string of the characters coming on serial
    }
    Serial.println(inputString);
    while (Serial.available() > 0)  
    { junk = Serial.read() ; }      // clear the serial buffer
    if(inputString.startsWith("a")){ 
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Alarm! Indringer");
      lcd.setCursor(0,2);
      lcd.print("gedetecteerd!");  
      digitalWrite(relay, HIGH);
      inputString = "";
    }else if(inputString.startsWith("u")){ 
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Het alarm is");
      lcd.setCursor(0,2);
      lcd.print("ingeschakeld.");
      inputString = ""; 
    }else if(inputString.startsWith("k")){ 
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Deze module is");
      lcd.setCursor(0,2);
      lcd.print("verbonden.");
      inputString = ""; 
    }else if(inputString.startsWith("o")){ 
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Het alarm is");
      lcd.setCursor(0,2);
      lcd.print("uitgeschakeld.");  
      digitalWrite(relay, LOW);
      inputString = "";
    }else if(inputString.startsWith("c")){ 
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Er is een module");
      lcd.setCursor(0,2);
      lcd.print("verbonden!");  
      digitalWrite(relay, LOW);
      inputString = "";
    }
    inputString = "";
  }
  if ( mfrc522.PICC_IsNewCardPresent()) {
        if ( mfrc522.PICC_ReadCardSerial())
        {
           if (mfrc522.uid.uidByte[0] == 0x26 && mfrc522.uid.uidByte[1] == 0x84 && mfrc522.uid.uidByte[2] == 0x90 && mfrc522.uid.uidByte[3] == 0xB9) {
      lcd.clear();
      Serial.println("g");
      digitalWrite(relay, LOW);
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Het alarm is");
      lcd.setCursor(0,2);
      lcd.print("uitgeschakeld.");
    } else {
      lcd.clear();
      lcd.print("Niet herkend.");
      lcd.setCursor(0,2);
      lcd.print("Niks gewijzigd.");
        }
}
}
}
