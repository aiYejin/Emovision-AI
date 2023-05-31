const int vibe_R = 2;
const int vibe_L = 4;

void setup() {
    pinMode(vibe_R, OUTPUT);
    pinMode(vibe_L, OUTPUT);
    Serial.begin(9600);
}

String pattern = "";
void loop() {
    if (Serial.available()) {
        char c = Serial.read();
        pattern += c;
        if (pattern == "jin") {
            // "jin"과 pattern이 동일한 경우
            digitalWrite(vibe_R, HIGH);
            delay(50);
            digitalWrite(vibe_R, LOW);
            delay(400);
            digitalWrite(vibe_R, HIGH);
            delay(50);
            digitalWrite(vibe_R, LOW);
            pattern = "";
        }
        else if (pattern == "eun") {
            // "eun"과 pattern이 동일한 경우
            digitalWrite(vibe_R, HIGH);
            delay(200);
            digitalWrite(vibe_R, LOW);
            delay(400);
            digitalWrite(vibe_R, HIGH);
            delay(200);
            digitalWrite(vibe_R, LOW);
            pattern = "";
        }
        else if (pattern == "N") {
            // "N"과 pattern이 동일한 경우
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
            pattern = "";
        }
        else if (pattern == "H") {
            // "H"과 pattern이 동일한 경우
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
            pattern = "";
        }
        else if (pattern == "F") {
            // "F"과 pattern이 동일한 경우
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
            pattern = "";
        }
        else if (pattern == "S") {
            // "S"과 pattern이 동일한 경우
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
            pattern = "";
        }
        else if (pattern == "sur") {
            // "sur"과 pattern이 동일한 경우
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
            pattern = "";
        }
    }
}
