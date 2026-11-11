package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"time"
)

func main() {
	args := os.Args[1:]

	if len(args) < 2 {
		return
	}

	count, err := strconv.Atoi(args[1])

	if err != nil {
		return
	}

	start := time.Now()
	buf := make([]byte, 512)
	var total = 0

	for i := 0; i < count; i++ {
		file, err := os.Open(args[0])

		if err != nil {
			fmt.Println("Error: ", err)
			return
		}

		scanner := bufio.NewReader(file)

		for {
			n, err := scanner.Read(buf)
			total += n
			if err == io.EOF {
				break
			}
			if err != nil {
				fmt.Fprintln(os.Stderr, err)
				os.Exit(1)
			}
		}

		file.Close()

	}

	elapsed := time.Since(start)

	fmt.Println(elapsed)
	fmt.Println(total)

}
