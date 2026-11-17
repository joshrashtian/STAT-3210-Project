package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"time"
)

const (
	chunk  = 65536
	warmup = 3
)

func readFile(path string, buf []byte) int {
	f, err := os.Open(path)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	defer f.Close()

	total := 0
	for {
		n, err := f.Read(buf)
		total += n
		if err == io.EOF {
			break
		}
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	}
	return total
}

func main() {
	if len(os.Args) < 3 {
		fmt.Fprintf(os.Stderr, "usage: %s <file> <iterations>\n", os.Args[0])
		os.Exit(1)
	}

	path := os.Args[1]
	iterations, err := strconv.Atoi(os.Args[2])
	if err != nil || iterations <= 0 {
		fmt.Fprintln(os.Stderr, "iterations must be a positive integer")
		os.Exit(1)
	}

	buf := make([]byte, chunk)

	size := 0
	for i := 0; i < warmup; i++ { // untimed: warms the cache
		size = readFile(path, buf)
	}

	times := make([]int64, iterations)
	for i := range times {
		t0 := time.Now()
		readFile(path, buf)
		times[i] = time.Since(t0).Nanoseconds()
	}

	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()
	fmt.Fprintln(out, size)
	for _, t := range times {
		fmt.Fprintln(out, t)
	}
}
