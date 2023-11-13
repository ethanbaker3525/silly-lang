#include <stdio.h>
#include <inttypes.h>

int64_t _entry();

void print_result(int64_t x)
{
  printf("%" PRId64, x);
}

int main(int argc, char** argv)
{
  int64_t result;

  result = _entry();
  print_result(result);
  putchar('\n');
  return 0;
}