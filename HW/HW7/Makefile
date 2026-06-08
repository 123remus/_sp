CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -pedantic
TARGET = mysh

all: $(TARGET)

$(TARGET): mysh.c
	$(CC) $(CFLAGS) -o $(TARGET) mysh.c

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run
