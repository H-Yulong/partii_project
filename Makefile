all : 
	gcc -c main.c
	gcc -o main main.c
	./main

clean: 
	rm main.o
	rm main
	rm main.exe.stackdump