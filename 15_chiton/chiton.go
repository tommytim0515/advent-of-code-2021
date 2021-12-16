package main

import (
	"fmt"
	"math"
	"os"
	"strings"
)

func getInputs(filename string) ([][]int, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	lines := strings.Split(string(data), "\n")
	inputs := make([][]int, len(lines))
	for i, line := range lines {
		line = strings.TrimSpace(line)
		fmt.Println(line)
		inputs[i] = make([]int, len(line))
		for j, c := range line {
			inputs[i][j] = int(c) - 48
		}
	}
	return inputs, nil
}

func lowestTotalRisk(riskMap [][]int) int {
	if riskMap == nil {
		return 0
	}
	if len(riskMap) == 0 {
		return 0
	}
	numRows := len(riskMap)
	numCols := len(riskMap[0])
	dijkstraMatrix := make([][]int, numRows)
	for i := 0; i < numRows; i++ {
		dijkstraMatrix[i] = make([]int, numCols)
		for j := 0; j < numCols; j++ {
			dijkstraMatrix[i][j] = math.MaxInt
		}
	}
	dijkstraMatrix[0][0] = 0
	visited := make(map[[2]int]bool)

	return 0
}

func main() {
	fmt.Println("Hello, world!")
	riskMap, err := getInputs("input.txt")
	if err != nil {
		panic(err)
	}
	fmt.Println(lowestTotalRisk(riskMap))
}
