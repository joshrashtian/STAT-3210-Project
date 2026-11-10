package main

import (
	"bufio"
	"fmt"
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

	var total = 0

	for i := 0; i < count; i++ {
		file, err := os.Open(args[0])

		if err != nil {
			fmt.Println("Error: ", err)
			return
		}

		scanner := bufio.NewScanner(file)

		for scanner.Scan() {
			total += 1
		}
		file.Close()

	}

	elapsed := time.Since(start)

	fmt.Println(elapsed)
	fmt.Println(total)

}
