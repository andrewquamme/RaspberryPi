#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wiringPi.h> // Include WiringPi Library

// ########   CUSTOMIZATIONS ####################
// Pin number declarations
const int BUZZER = 19;  // Buzzer pin
const int LED    = 21;  // LED pin
const int SPEED  = 60;  // CW Speed
// ##############################################

// CW constants
const int DOT    = SPEED;
const int SYMBOL = SPEED;
const int DASH   = SPEED * 3;
const int LETTER = SPEED * 3;
const int WORD   = SPEED * 7;

void convert_to_morse(char s[]);
void play_morse();

char morse[] = "";
const int MAX_LEN       = 51;
const int NUM_OFFSET    = 44;
const int LETTER_OFFSET = 65;

char *letters[26] = {".-" ,"-...", "-.-.", "-..", ".",  // A-E
    "..-.", "--.", "....", "..", ".---",                // F-J
    "-.-", ".-..", "--", "-.", "---",                   // H-O
    ".--.", "--.-", ".-.", "...", "-",                  // P-T
    "..-", "...-", ".--", "-..-", "-.--",               // U-Y
    "--.."};                                            // Z

// , ? . / 0 1 2 3 4 5 6 7 8 9
char *symNum[14]  = {"--..--", "..--..", ".-.-.-", "-..-." ,"-----",
    ".----", "..---", "...--", "....-", ".....",
    "-....", "--..." ,"---..", "----."};

int main(void) {

    // Setup GPIO
    wiringPiSetupGpio(); // Initialize wiringPi -- (Broadcom)
    // pinMode(BUZZER, OUTPUT);  // Set BUZZER as output
    pinMode(LED, OUTPUT); // Set  LED as output
    printf("GPIO setup complete\n");

    while(1) {
        char string[MAX_LEN];
        strcpy(morse, "");
        printf("Enter a string (ctrl+c to exit): ");
        fgets(string, MAX_LEN, stdin);
        // char string[] = "cq cq cq, de K7ASQ. qrz?";
        printf("%s\n",string);

        convert_to_morse(string);
        printf("%s\n", morse);
        play_morse(morse);
    }

    return 0;
}

void convert_to_morse(char s[]) {

    strcat(morse, "||");

    for (int i = 0; i<strlen(s); i++) {

        if (s[i] == 44) {                   // comma
            strcat(morse, symNum[0]);
            strcat(morse, "|");
        }
        else if (s[i] > 45 && s[i] < 58) {  // symbols & numbers
            strcat(morse, symNum[s[i] - NUM_OFFSET]);
            strcat(morse, "|");
        }
        else if (s[i] == 32) {              // space
            strcat(morse, " ");
            strcat(morse, "|");
        }
        else if (s[i] == 63) {              // question mark
            strcat(morse, symNum[1]);
            strcat(morse, "|");
        }
        else if (s[i] > 64 && s[i] < 91) {  // uppercase letters
            strcat(morse, letters[s[i] - LETTER_OFFSET]);
            strcat(morse, "|");
        }
        else if (s[i] > 96 && s[i] < 123) { // lowercase letters
            strcat(morse, letters[s[i] - 32 - LETTER_OFFSET]);
            strcat(morse, "|");
        }
        else {
            strcat(morse, "|");
        }
    }
}

void play_morse(char s[]) {

    printf("Playing Morse...");

    for (int i = 0; i<strlen(s); i++) {
        if (s[i] == '.') {
            // printf("%s", "dit");

            // digitalWrite(BUZZER, HIGH);
            digitalWrite(LED, HIGH);
            delay(DOT);
            // digitalWrite(BUZZER, LOW);
            digitalWrite(LED, LOW);
            delay(SYMBOL);
        }
        else if (s[i] == '-') {
            // printf("%s", "dah");

            // digitalWrite(BUZZER, HIGH);
            digitalWrite(LED, HIGH);
            delay(DASH);
            // digitalWrite(BUZZER, LOW);
            digitalWrite(LED, LOW);
            delay(SYMBOL);
        }
        else if (s[i] == '|') {
            // printf("%s", " ");
            delay(LETTER);
        }
        else if (s[i] == ' ') {
            // printf("%s", "\n");
            delay(WORD);
        }

    }
    printf("\n");
}