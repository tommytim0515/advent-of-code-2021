package main

import (
	"fmt"
	"os"
	"strings"
)

var (
	startNotation string = "start"
	endNotation   string = "end"
)

func indexOf(s []string, e string) int {
	for i, a := range s {
		if a == e {
			return i
		}
	}
	return -1
}

func getInputs(filename string) ([][]int, []string, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, nil, err
	}
	lines := strings.Split(string(data), "\n")
	pointMap := make(map[string]bool)
	for _, line := range lines {
		line = strings.TrimSpace(line)
		twoPoints := strings.Split(line, "-")
		for _, point := range twoPoints {
			if _, ok := pointMap[point]; !ok {
				pointMap[point] = true
			}
		}
	}
	points := make([]string, 0, len(pointMap))
	for point := range pointMap {
		points = append(points, point)
	}
	vertices := make([][]int, len(points))
	for i := range vertices {
		vertices[i] = make([]int, len(points))
	}
	for _, line := range lines {
		line = strings.TrimSpace(line)
		twoPoints := strings.Split(line, "-")
		vertices[indexOf(points, twoPoints[0])][indexOf(points, twoPoints[1])] = 1
		vertices[indexOf(points, twoPoints[1])][indexOf(points, twoPoints[0])] = 1
	}
	return vertices, points, nil
}

func getNumPaths(vertices [][]int, points []string, point string,
	visited map[string]bool) int {
	if point == endNotation {
		return 1
	}
	if strings.ToLower(point) == point {
		visited[point] = true
	}
	numPaths := 0
	idx := indexOf(points, point)
	for i := range vertices[idx] {
		_, ok := visited[points[i]]
		if vertices[idx][i] == 1 && !ok {
			newVisited := make(map[string]bool)
			for k, v := range visited {
				newVisited[k] = v
			}
			numPaths += getNumPaths(vertices, points, points[i], newVisited)
		}
	}
	return numPaths
}

func getNumPathsPro(vertices [][]int, points []string, point string,
	visited map[string]bool, used bool) int {
	if point == endNotation {
		return 1
	}
	if strings.ToLower(point) == point {
		visited[point] = true
	}
	numPaths := 0
	idx := indexOf(points, point)
	for i := range vertices[idx] {
		if vertices[idx][i] == 0 {
			continue
		}
		_, ok := visited[points[i]]
		newVisited := make(map[string]bool)
		for k, v := range visited {
			newVisited[k] = v
		}
		if !ok {
			numPaths += getNumPathsPro(vertices, points, points[i], newVisited, used)
		} else if !used && points[i] != startNotation && points[i] != endNotation {
			numPaths += getNumPathsPro(vertices, points, points[i], newVisited, true)
		}
	}
	return numPaths
}

func main() {
	vertices, points, err := getInputs("input.txt")
	if err != nil {
		panic(err)
	}
	for _, line := range vertices {
		fmt.Println(line)
	}
	fmt.Println(points)
	fmt.Printf("Number of paths %d\n", getNumPaths(vertices, points,
		startNotation, make(map[string]bool)))
	fmt.Printf("Number of paths %d\n", getNumPathsPro(vertices, points,
		startNotation, make(map[string]bool), false))
}
