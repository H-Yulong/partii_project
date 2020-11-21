all : 
	gcc -c utils.c
	gcc -c main.c
	gcc -o Outputs/main utils.o main.o
	Outputs/main

clean: 
	rm main.o
	rm utils.o
	rm main.exe.stackdump