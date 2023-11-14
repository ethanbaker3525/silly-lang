#include <stdio.h>
#include <inttypes.h>

extern int64_t _entry();
extern long _type;

void print_result(int64_t x, int64_t t) {
  switch(t) {
    case 0:
      printf("%" PRId64, x);
      break;
    case 1:
      if (x == 0) {
        printf("false");
      } else {
        printf("true");
      }
      break;
    case 2:
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