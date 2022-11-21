#include <wiringPi.h>
#include <stdio.h>
#include <string.h>

#define RED_PIN 3

int turn_on(){
	printf("%s\n", "Red Light ON!");
	digitalWrite(RED_PIN, HIGH);
	
	return 0;
}

int turn_off(){
	printf("%s\n", "Red Light OFF!");
	digitalWrite(RED_PIN, LOW);
	
	return 0;
}

int init() {
	printf("%s\n", "Init Light!");
	digitalWrite(RED_PIN, HIGH);
	delay(500);
	digitalWrite(RED_PIN, LOW);
	delay(500);
}

int main (int argc,char *argv[])
{
	int i;
    for (i=0; i < argc; i++)
        printf("Argument %d is %s\n", i, argv[i]);
	
	wiringPiSetup() ;
	pinMode(RED_PIN, OUTPUT) ;

	if(argc == 2){
		char* comm = argv[1];
		
		if(strcmp(comm, "1") == 0){
			turn_on();
		} else if(strcmp(comm, "2") == 0){
			turn_off();
		}else if(strcmp(comm, "0") == 0){
			init();
		}
	}

	return 0 ;
}
