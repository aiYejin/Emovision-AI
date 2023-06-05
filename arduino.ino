const int vibe_R = 2;
const int vibe_L = 4;
const int switchPin = 7;

void setup(){
    pinMode(vibe_R, OUTPUT);
    pinMode(vibe_L, OUTPUT);
    pinMode(switchPin, INPUT);
    Serial.begin(9600);
}


void loop() {
    int switchState = digitalRead(switchPin);
    if (Serial.available()) {
        char pattern = Serial.read();
        Serial.print("My character: ");
        Serial.println(pattern); // 문자 출력
        if (pattern == 'J') {
            // 'J'과 pattern이 동일한 경우
            digitalWrite(vibe_R, HIGH);
            delay(50);
            digitalWrite(vibe_R, LOW);
            delay(400);
            digitalWrite(vibe_R, HIGH);
            delay(50);
            digitalWrite(vibe_R, LOW);
        }
        if (pattern == 'E') {
            // 'E'과 pattern이 동일한 경우
            digitalWrite(vibe_R, HIGH);
            delay(200);
            digitalWrite(vibe_R, LOW);
            delay(400);
            digitalWrite(vibe_R, HIGH);
            delay(200);
            digitalWrite(vibe_R, LOW);
        }
        if (switchState == LOW) {  // 스위치가 ON인 경우
            if (pattern == 'N') {
                // 'N'과 pattern이 동일한 경우
                digitalWrite(vibe_L, HIGH);
                delay(200);
                digitalWrite(vibe_L, LOW);
                delay(400);
                digitalWrite(vibe_L, HIGH);
                delay(200);
                digitalWrite(vibe_L, LOW);
                delay(400);
                digitalWrite(vibe_L, HIGH);
                delay(200);
                digitalWrite(vibe_L, LOW);
            }
            if (pattern == 'H') {
                // 'H'과 pattern이 동일한 경우
                digitalWrite(vibe_L, HIGH);
                delay(50);
                digitalWrite(vibe_L, LOW);
                delay(400);
                digitalWrite(vibe_L, HIGH);
                delay(200);
                digitalWrite(vibe_L, LOW);
                delay(400);
                digitalWrite(vibe_L, HIGH);
                delay(200);
                digitalWrite(vibe_L, LOW);
            }
            if (pattern == 'F') {
                // 'F'과 pattern이 동일한 경우
                digitalWrite(vibe_L, HIGH);
                delay(50);
                digitalWrite(vibe_L, LOW);
                delay(400);
                digitalWrite(vibe_L, HIGH);
                delay(50);
                digitalWrite(vibe_L, LOW);
                delay(400);
                digitalWrite(vibe_L, HIGH);
                delay(50);
                digitalWrite(vibe_L, LOW);
            }
            if (pattern == 'S') {
                // 'S'과 pattern이 동일한 경우
                digitalWrite(vibe_L, HIGH);
                delay(200);
                digitalWrite(vibe_L, LOW);
                delay(400);
                digitalWrite(vibe_L, HIGH);
                delay(200);
                digitalWrite(vibe_L, LOW);
                delay(400);
                digitalWrite(vibe_L, HIGH);
                delay(50);
                digitalWrite(vibe_L, LOW);
            }
            if (pattern == 'U') {
                // 'sur'과 pattern이 동일한 경우
                digitalWrite(vibe_L, HIGH);
                delay(200);
                digitalWrite(vibe_L, LOW);
                delay(400);
                digitalWrite(vibe_L, HIGH);
                delay(50);
                digitalWrite(vibe_L, LOW);
                delay(400);
                digitalWrite(vibe_L, HIGH);
                delay(200);
                digitalWrite(vibe_L, LOW);
            }
        }
    }
}
