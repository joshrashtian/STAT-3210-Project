#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define CHUNK 65536
#define WARMUP 3

static uint64_t now_ns(void) {
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

static size_t read_file(const char *path, char *buf) {
  FILE *fp = fopen(path, "rb");
  if (fp == NULL) {
    perror(path);
    exit(1);
  }
  size_t total = 0, n;
  while ((n = fread(buf, 1, CHUNK, fp)) > 0)
    total += n;
  fclose(fp);
  return total;
}

int main(int argc, char **argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: %s <file> <iterations>\n", argv[0]);
    return 1;
  }

  int iter = atoi(argv[2]);
  if (iter <= 0) {
    fprintf(stderr, "iterations must be > 0\n");
    return 1;
  }

  char *buf = malloc(CHUNK);
  uint64_t *times = malloc((size_t)iter * sizeof *times);
  if (buf == NULL || times == NULL)
    return 1;

  size_t size = 0;
  for (int i = 0; i < WARMUP; i++) // untimed: warms the cache
    size = read_file(argv[1], buf);

  for (int i = 0; i < iter; i++) {
    uint64_t t0 = now_ns();
    read_file(argv[1], buf);
    times[i] = now_ns() - t0;
  }

  printf("%zu\n", size);
  for (int i = 0; i < iter; i++)
    printf("%llu\n", (unsigned long long)times[i]);

  free(times);
  free(buf);
  return 0;
}
