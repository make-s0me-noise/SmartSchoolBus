#include <wiringPi.h>
#include <stdio.h>
#include <string.h>

#define RED_PIN 27
#define BLUE_PIN 29
#define GREEN_PIN 28

int turn_off(){
   digitalWrite(RED_PIN, LOW);
   digitalWrite(GREEN_PIN, LOW);
   digitalWrite(BLUE_PIN, LOW);
   
   return 0;
}

int turn_on_red(){
   turn_off();
   digitalWrite(RED_PIN, HIGH);
   
   return 0;
}

int turn_on_green(){
   turn_off();
   digitalWrite(GREEN_PIN, HIGH);
   
   return 0;
}

int turn_on_purple(){
    turn_off();
    digitalWrite(RED_PIN, HIGH);
    digitalWrite(BLUE_PIN, HIGH);
}

int init() {
   digitalWrite(RED_PIN, HIGH);
   delay(500);
   digitalWrite(RED_PIN, LOW);
   delay(500);
}

int main (int argc,char *argv[])
{
   int i;
   
   wiringPiSetup() ;
   pinMode(RED_PIN, OUTPUT) ;
   pinMode(GREEN_PIN, OUTPUT);
   pinMode(BLUE_PIN, OUTPUT);

   if(argc == 2){
      char* comm = argv[1];
      
      if(strcmp(comm, "1") == 0){
         turn_on_red();
      } else if(strcmp(comm, "2") == 0){
         turn_on_green();
      }else if(strcmp(comm, "3") == 0){
         turn_on_purple();
      }else if(strcmp(comm, "4") == 0){
         turn_off();
      }else if(strcmp(comm, "0") == 0){
         init();
      }
   }

   return 0 ;
}