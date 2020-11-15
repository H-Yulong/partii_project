all : 
	gcc -c main.c
	gcc -o main main.c

clean: 
	rm main.o
	rm main