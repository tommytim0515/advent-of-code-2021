package main

import (
	"fmt"
	"os"
	"sort"
	"strings"
)

func getInputs(filename string) ([][]int, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	lines := strings.Split(string(data), "\n")
	mapData := make([][]int, len(lines))
	for i := range mapData {
		mapData[i] = make([]int, len(lines[i]))
	}
	for i := range lines {
		for j := range lines[i] {
			mapData[i][j] = int(lines[i][j] - '0')
		}
	}
	return mapData, nil
}

func sumLowPointRiskLevel(mapData [][]int) int {
	riskLevel := 0
	for i := range mapData {
		for j := range mapData[i] {
			if i-1 >= 0 && mapData[i-1][j] <= mapData[i][j] {
				continue
			}
			if i+1 < len(mapData) && mapData[i+1][j] <= mapData[i][j] {
				continue
			}
			if j-1 >= 0 && mapData[i][j-1] <= mapData[i][j] {
				continue
			}
			if j+1 < len(mapData[i]) && mapData[i][j+1] <= mapData[i][j] {
				continue
			}
			riskLevel += (mapData[i][j] + 1)
		}
	}
	return riskLevel
}

func initMapData(mapData [][]int) {
	for i := range mapData {
		for j := range mapData[i] {
			if mapData[i][j] == 9 {
				mapData[i][j] = 1
			} else {
				mapData[i][j] = 0
			}
		}
	}
}

func tagBasin(mapData [][]int, i, j int) int {
	if mapData[i][j] != 0 {
		return 0
	}
	mapData[i][j] = 1
	res := 1
	if i-1 >= 0 {
		res += tagBasin(mapData, i-1, j)
	}
	if i+1 < len(mapData) {
		res += tagBasin(mapData, i+1, j)
	}
	if j-1 >= 0 {
		res += tagBasin(mapData, i, j-1)
	}
	if j+1 < len(mapData[i]) {
		res += tagBasin(mapData, i, j+1)
	}
	return res
}

func multiplicationThreeLargestBasins(mapData [][]int) int {
	initMapData(mapData)
	var topThree []int
	for i := range mapData {
		for j := range mapData[i] {
			if mapData[i][j] != 0 {
				continue
			}
			sizeBasin := tagBasin(mapData, i, j)
			if len(topThree) < 3 {
				topThree = append(topThree, sizeBasin)
			} else {
				sort.Ints(topThree)
				if sizeBasin > topThree[0] {
					topThree[0] = sizeBasin
				}
			}
		}
	}
	return topThree[0] * topThree[1] * topThree[2]
}

func main() {
	mapData, err := getInputs("input.txt")
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("Sum of risk level: %d\n", sumLowPointRiskLevel(mapData))
	fmt.Printf("Multiplication of the sizes of top 3 basins %d\n",
		multiplicationThreeLargestBasins(mapData))
}
