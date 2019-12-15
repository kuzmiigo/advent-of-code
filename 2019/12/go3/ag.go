package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
	"strings"
)

const dimensions = 3

var numberPattern = regexp.MustCompile(`[\-\d]+`)

func main() {
	positions := parseData(readFile())
	n := len(positions[0])
	initialPositions := duplicate(positions)
	velocities := makeMatrix(dimensions, n)

	ch := make(chan int64, dimensions)

	for d := 0; d < dimensions; d++ {
		go func(p, ip, v []int) {
			for steps := int64(1); ; steps++ {
				step(p, v)
				if hasAlignment(p, ip, v) {
					ch <- steps
					return
				}
			}
		}(positions[d], initialPositions[d], velocities[d])
	}

	var stepsToReachAlignment int64 = 1
	for d := 0; d < dimensions; d++ {
		stepsToReachAlignment = lcm(stepsToReachAlignment, <-ch)
	}
	fmt.Println(stepsToReachAlignment)
}

func step(positions, velocities []int) {
	n := len(positions)
	// Adjust velocity
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			gravity := sign(positions[j] - positions[i])
			velocities[i] += gravity
			velocities[j] -= gravity
		}
	}
	// Apply velocity
	for i := 0; i < n; i++ {
		positions[i] += velocities[i]
	}
}

func hasAlignment(positions, initialPositions, velocities []int) bool {
	for i, x := range initialPositions {
		if positions[i] != x {
			return false
		}
		if velocities[i] != 0 {
			return false
		}
	}
	return true
}

func readFile() string {
	filename := "input.txt"
	if len(os.Args) > 1 {
		filename = os.Args[1]
	}

	input, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return string(input)
}

func parseData(input string) [][]int {
	moonSpecs := strings.Split(input, "\n")
	moons := makeMatrix(dimensions, 0)

	for _, ms := range moonSpecs {
		coordinates := getCoordinates(ms)
		if len(coordinates) != dimensions {
			continue
		}
		for i, c := range coordinates {
			moons[i] = append(moons[i], c)
		}
	}
	return moons
}

func sign(x int) int {
	if x < 0 {
		return -1
	}
	if x > 0 {
		return 1
	}
	return 0
}

func getCoordinates(moonSpec string) []int {
	numberStrings := numberPattern.FindAllString(moonSpec, -1)
	numbers := make([]int, len(numberStrings))
	for i, numberString := range numberStrings {
		number, err := strconv.Atoi(numberString)
		if err != nil {
			panic(err)
		}
		numbers[i] = number
	}
	return numbers
}

func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func lcm(a, b int64) int64 {
	m := a * b
	if m < 0 {
		m = -m
	}
	return m / gcd(a, b)
}

func makeMatrix(m, n int) [][]int {
	a := make([][]int, m)
	for i := range a {
		a[i] = make([]int, n)
	}
	return a
}

func duplicate(matrix [][]int) [][]int {
	d := make([][]int, len(matrix))
	for i := range matrix {
		d[i] = make([]int, len(matrix[i]))
		copy(d[i], matrix[i])
	}
	return d
}
