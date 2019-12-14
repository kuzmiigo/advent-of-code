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

	moons, moonInitialStates := parseData(readFile())

	for alignmentsFound < 3 {
		steps++

		adjustAllVelocity(moons)
		for _, m := range moons {
			applyVelocity(m)
		}

		hasAlignment := []bool{true, true, true}
		for d := 0; d < 3; d++ {
			for i := 0; i < len(moons) && hasAlignment[d]; i++ {
				moon := moons[i]
				if moon.coordinates[d] != moonInitialStates[i][d] {
					hasAlignment[d] = false
				}
				if moon.velocities[d] != 0 {
					hasAlignment[d] = false
				}

			}
		}

		for d := 0; d < 3; d++ {
			if hasAlignment[d] && alignments[d] == 0 {
				alignments[d] = steps
				alignmentsFound++
			}
		}
	}

	stepsToReachAlignment := lcm(alignments...)
	fmt.Println(stepsToReachAlignment)
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

func parseData(input string) ([]*moon, [][]int) {
	var moons []*moon
	var moonInitialStates [][]int

	moonSpecs := strings.Split(input, "\n")

	for _, ms := range moonSpecs {
		coordinates := getCoordinates(ms)
		if len(coordinates) == 0 {
			continue
		}
		initialCoordinates := make([]int, len(coordinates))
		copy(initialCoordinates, coordinates)
		m := moon{
			coordinates: coordinates,
			velocities:  make([]int, 3),
		}
		moons = append(moons, &m)
		moonInitialStates = append(moonInitialStates, initialCoordinates)
	}
	return moons, moonInitialStates
}

func adjustAllVelocity(moons []*moon) {
	for c := range combinations(len(moons), 2) {
		adjustVelocity(moons[c[0]], moons[c[1]])
	}
}

func adjustVelocity(m1 *moon, m2 *moon) {
	for d := 0; d < 3; d++ {
		if m1.coordinates[d] > m2.coordinates[d] {
			m1.velocities[d]--
			m2.velocities[d]++
		} else if m1.coordinates[d] < m2.coordinates[d] {
			m1.velocities[d]++
			m2.velocities[d]--
		}
	}
}

func adjustAllVelocity2(moons []*moon) {
	for _, m1 := range moons {
		for _, m2 := range moons {
			if m1 != m2 {
				adjustVelocity2(m1, m2)
			}
		}
	}
}

func adjustVelocity2(m1 *moon, m2 *moon) {
	for d := 0; d < 3; d++ {
		if m1.coordinates[d] > m2.coordinates[d] {
			m1.velocities[d]--
		} else if m1.coordinates[d] < m2.coordinates[d] {
			m1.velocities[d]++
		}
	}
}

func applyVelocity(m *moon) {
	for d := 0; d < 3; d++ {
		m.coordinates[d] += m.velocities[d]
	}
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

func combinations(n, length int) <-chan []int {
	c := make(chan []int)
	var rc func(int, int, []int)
	rc = func(i, next int, combination []int) {
		if i == length {
			c <- combination
			return
		}
		for j := next; j < n; j++ {
			rc(i+1, j+1, append(combination, j))
		}
		return
	}
	go func(c chan []int) {
		defer close(c)
		rc(0, 0, make([]int, 0))
	}(c)

	return c
}
