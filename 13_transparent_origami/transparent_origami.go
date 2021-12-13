package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func getInputs(filename string) ([][]int, [][]int, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, nil, err
	}
	lines := strings.Split(string(data), "\n")
	var (
		points [][]int
		folds  [][]int
		idx    int
	)
	for {
		striped := strings.TrimSpace(lines[idx])
		if striped == "" {
			idx++
			break
		}
		coors := strings.Split(striped, ",")
		coorX, err := strconv.Atoi(coors[0])
		if err != nil {
			return nil, nil, err
		}
		coorY, err := strconv.Atoi(coors[1])
		if err != nil {
			return nil, nil, err
		}
		points = append(points, []int{coorX, coorY})
		idx++
	}
	for {
		if idx >= len(lines) {
			break
		}
		striped := strings.TrimSpace(lines[idx])
		segments := strings.Split(striped, "=")
		distance, err := strconv.Atoi(segments[1])
		if err != nil {
			return nil, nil, err
		}
		if strings.Contains(segments[0], "x") {
			folds = append(folds, []int{0, distance})
		} else {
			folds = append(folds, []int{1, distance})
		}
		idx++
	}
	return points, folds, nil
}

func firstFold(points [][]int, fold []int) int {
	pointMap := make(map[[2]int]bool)
	if fold[0] == 0 {
		for _, point := range points {
			if point[0] > fold[1] {
				pointMap[[2]int{2*fold[1] - point[0], point[1]}] = true
			} else {
				pointMap[[2]int{point[0], point[1]}] = true
			}
		}
	} else {
		for _, point := range points {
			if point[1] > fold[1] {
				pointMap[[2]int{point[0], 2*fold[1] - point[1]}] = true
			} else {
				pointMap[[2]int{point[0], point[1]}] = true
			}
		}
	}
	return len(pointMap)
}

func getCode(points [][]int, folds [][]int) [][]rune {
	var pointList [][]int
	for _, point := range points {
		pointList = append(pointList, point)
	}
	for _, fold := range folds {
		pointMap := make(map[[2]int]bool)
		if fold[0] == 0 {
			for _, point := range pointList {
				if point[0] > fold[1] {
					pointMap[[2]int{2*fold[1] - point[0], point[1]}] = true
				} else {
					pointMap[[2]int{point[0], point[1]}] = true
				}
			}
		} else {
			for _, point := range pointList {
				if point[1] > fold[1] {
					pointMap[[2]int{point[0], 2*fold[1] - point[1]}] = true
				} else {
					pointMap[[2]int{point[0], point[1]}] = true
				}
			}
		}
		pointList = make([][]int, 0)
		for point := range pointMap {
			pointList = append(pointList, []int{point[0], point[1]})
		}
	}
	var (
		maxX int
		minX int
		maxY int
		minY int
	)
	for _, point := range pointList {
		if point[0] > maxX {
			maxX = point[0]
		}
		if point[0] < minX {
			minX = point[0]
		}
		if point[1] > maxY {
			maxY = point[1]
		}
		if point[1] < minY {
			minY = point[1]
		}
	}
	matrix := make([][]rune, maxY+1)
	for i := 0; i < maxY-minY+1; i++ {
		matrix[i] = make([]rune, maxX-minX+1)
		for j := 0; j < maxX+1; j++ {
			matrix[i+minY][j+minY] = ' '
		}
	}
	for _, point := range pointList {
		matrix[point[1]+minY][point[0]+minX] = '#'
	}
	return matrix
}

func main() {
	points, folds, err := getInputs("input.txt")
	if err != nil {
		panic(err)
	}
	fmt.Println(firstFold(points, folds[0]))
	matrix := getCode(points, folds)
	for _, row := range matrix {
		for _, val := range row {
			fmt.Printf("%s ", string(val))
		}
		fmt.Println()
	}
}
