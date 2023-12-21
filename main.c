#include <stdio.h>
#include <inttypes.h>

extern int64_t _entry();
extern long _type;

char read_byte() {
  char c = getc(stdin);
  return c;
}

char peek_byte() {
  char c = getc(stdin);
  ungetc(c, stdin);
  return c;
}

void write_byte(char c) {
  putc(c, stdout);
}

void print_result(int64_t x, int64_t t) {
  switch(t) {
    case 2:
      printf("%" PRId64, x);
      break;
    case 1:
      if (x == 0) {
        printf("false");
      } else {
        printf("true");
      }
      break;
    case 3:
      printf("%c", x);
      break;
  }
}

int main(int argc, char** argv) {
  int64_t result = _entry();
  print_result(result, _type);
  putchar('\n');
  return 0; // exit code
}