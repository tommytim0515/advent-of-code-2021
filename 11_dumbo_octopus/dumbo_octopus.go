package main

import (
	"fmt"
	"os"
	"strings"
)

func getInputs(filename string) ([][]int, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	var res [][]int
	for _, line := range strings.Split(string(data), "\r\n") {
		row := make([]int, 10)
		for i := 0; i < 10; i++ {
			row[i] = int(line[i] - '0')
		}
		res = append(res, row)
	}
	return res, nil
}

func octopusFlashNeighbor(octMap [][]int, i int, j int) int {
	var numFlashes int
	for a := i - 1; a <= i+1; a++ {
		for b := j - 1; b <= j+1; b++ {
			if a == i && b == j {
				continue
			}
			if a < 0 || a >= len(octMap) || b < 0 || b >= len(octMap[a]) {
				continue
			}
			if octMap[a][b] == -1 {
				continue
			}
			octMap[a][b]++
			if octMap[a][b] > 9 {
				octMap[a][b] = -1
				numFlashes++
				numFlashes += octopusFlashNeighbor(octMap, a, b)
			}
		}
	}
	return numFlashes
}

func countFlashes(octMap [][]int, itr int) int {
	var numFlashes int
	for dump := 0; dump < itr; dump++ {
		for i := 0; i < len(octMap); i++ {
			for j := 0; j < len(octMap[i]); j++ {
				if octMap[i][j] == -1 {
					continue
				}
				octMap[i][j]++
				if octMap[i][j] > 9 {
					octMap[i][j] = -1
					numFlashes++
					numFlashes += octopusFlashNeighbor(octMap, i, j)
				}
			}
		}
		for i := 0; i < len(octMap); i++ {
			for j := 0; j < len(octMap[i]); j++ {
				if octMap[i][j] == -1 {
					octMap[i][j] = 0
				}
			}
		}
	}
	return numFlashes
}

func allFlashCount(octMap [][]int) int {
	var cnt int
	for {
		for i := 0; i < len(octMap); i++ {
			for j := 0; j < len(octMap[i]); j++ {
				if octMap[i][j] == -1 {
					continue
				}
				octMap[i][j]++
				if octMap[i][j] > 9 {
					octMap[i][j] = -1
					octopusFlashNeighbor(octMap, i, j)
				}
			}
		}
		var sumFlashes int
		for i := 0; i < len(octMap); i++ {
			for j := 0; j < len(octMap[i]); j++ {
				if octMap[i][j] == -1 {
					octMap[i][j] = 0
					sumFlashes++
				}
				if sumFlashes == 100 {
					return cnt + 1
				}
			}
		}
		cnt++
	}
}

func main() {
	inputs, err := getInputs("input.txt")
	if err != nil {
		panic(err)
	}
	fmt.Println(countFlashes(inputs, 100))
	inputs, err = getInputs("input.txt")
	if err != nil {
		panic(err)
	}
	fmt.Println(allFlashCount(inputs))
}
