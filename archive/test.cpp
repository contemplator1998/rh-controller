#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>    
#include <iostream>
#include <stdio.h>      // standard input / output functions
#include <stdlib.h>
#include <string.h>     // string function definitions
#include <unistd.h>     // UNIX standard function definitions
#include <fcntl.h>      // File control definitions
#include <errno.h>      // Error number definitions
#include <termios.h>    // POSIX terminal control definitions

int main() {
	char byte;
	int USB = open("/dev/ttyUSB0", O_RDWR| O_NOCTTY);

	struct termios tty;
	struct termios tty_old;
	memset (&tty, 0, sizeof tty);


	/* Make raw */
	cfmakeraw(&tty);

	/* Flush Port, then applies attributes */
	tcflush( USB, TCIFLUSH );
	if ( tcsetattr ( USB, TCSANOW, &tty ) != 0) {
	   std::cout << "Error " << errno << " from tcsetattr" << std::endl;
	}    
	    

	/* Set Baud Rate */
	cfsetospeed (&tty, (speed_t)B115200);
	cfsetispeed (&tty, (speed_t)B115200);

	char* text = new char[2];
	text[0] = 207;
	text[2] = 0;
	write(USB, text, 1);
	std::cout << "Servo selected..." << std::endl; 
	int a = 2, b = 3;
	for (int i = 0; i < 100000000; i++) {
	a += b;
	}
	text[0] = 201;
	write(USB, text, 1);
	std::cout << "Angle selected..." << std::endl;
	for (int i = 0; i < 100000000; i++) {
	a += b;
	}
	text[0] = 180;
	write(USB, text, 1);
	std::cout << "Angle sent..." << std::endl;
	return 0;
}
