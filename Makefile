CC=gcc
CFLAGS=-I.
DEPS=rngs.h
OBJ=rngs.o projectile-template.o

%.o: %.c $(DEPS)
		$(CC) -c -o $@ $< $(CFLAGS)

project: $(OBJ)
		$(CC) -o $@ $^ $(CFLAGS)

clean: 
	rm -f *.o project
