package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
	"strings"
)

var (
	numberPattern = regexp.MustCompile(`[\-\d]+`)
)

type moon struct {
	coordinates []int
	velocities  []int
}

func main() {
	var steps int64
	var alignmentsFound int
	alignments := make([]int64, 3)

	positions := parseData(readFile())
	n := len(positions[0])
	initialPositions := duplicate(positions)
	velocities := makeMatrix(3, n)

	for alignmentsFound < 3 {
		steps++
		step(positions, velocities)

		for d := 0; d < 3; d++ {
			if alignments[d] != 0 {
				continue
			}
			if hasAlignment(d, positions, initialPositions, velocities) {
				alignments[d] = steps
				alignmentsFound++
			}
		}
	}

	stepsToReachAlignment := lcm(alignments...)
	fmt.Println(stepsToReachAlignment)
}

func step(positions, velocities [][]int) {
	n := len(positions[0])
	for d := 0; d < 3; d++ {
		// Adjust velocity
		p := positions[d]
		v := velocities[d]
		for i := 0; i < n; i++ {
			for j := i + 1; j < n; j++ {
				gravity := sign(p[j] - p[i])
				v[i] += gravity
				v[j] -= gravity
			}
		}
		// Apply velocity
		for i := 0; i < n; i++ {
			p[i] += v[i]
		}
	}
}

func hasAlignment(dim int, pos, initialPos, vel [][]int) bool {
	for i, x := range initialPos[dim] {
		if pos[dim][i] != x {
			return false
		}
		if vel[dim][i] != 0 {
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
	moons := makeMatrix(3, 0)

	for _, ms := range moonSpecs {
		coordinates := getCoordinates(ms)
		if len(coordinates) != 3 {
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

func lcm(integers ...int64) int64 {
	var result int64 = 1
	for _, x := range integers {
		result = result * x / gcd(result, x)
	}
	return result
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
