#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define BYTE_SIZE 512

double now_ns(void) {
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return ts.tv_sec * 1e9 + ts.tv_nsec;
}
int main(int argc, char **argv) {

  if (argc < 3)
    return 1;

  char *buffer = malloc(BYTE_SIZE + 1);
  if (buffer == NULL) {
    return 1;
  }

  int iter = atoi(argv[2]);

  size_t total = 0;
  double start = now_ns();

  for (int i = 0; i < iter; i++) {
    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL) {
      free(buffer);
      return 1;
    }

    size_t n;
    while ((n = fread(buffer, 1, BYTE_SIZE, fp)) > 0)
      total += n;
    fclose(fp);
  }

  double elapsed = now_ns() - start;
  printf("total: %zu\n", total);
  printf("time: %.3f ms\n", elapsed / 1e6);
  free(buffer);
  return 0;
}
