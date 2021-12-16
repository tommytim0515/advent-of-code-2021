package main

import (
	"fmt"
	"math"
	"os"
	"strings"
)

func getInputs(filename string) (string, map[string]rune, error) {
	rules := make(map[string]rune)
	data, err := os.ReadFile(filename)
	if err != nil {
		return "", nil, err
	}
	lines := strings.Split(string(data), "\n")
	for i := 2; i < len(lines); i++ {
		segments := strings.Split(lines[i], " -> ")
		rules[segments[0]] = rune(segments[1][0])
	}
	return lines[0], rules, nil
}

func pairInsertion(polymer string, rules map[string]rune, steps int) int {
	var newPolymer string
	for i := 0; i < steps; i++ {
		for j := 0; j < len(polymer)-1; j++ {
			newPolymer += string(polymer[j])
			newPolymer += string(rules[polymer[j:j+2]])
		}
		newPolymer += string(polymer[len(polymer)-1])
		polymer = newPolymer
		newPolymer = ""
	}
	charCounts := make(map[rune]int)
	for _, char := range polymer {
		if _, ok := charCounts[char]; ok {
			charCounts[char]++
		} else {
			charCounts[char] = 1
		}
	}
	maxCount := 0
	minCount := len(polymer)
	for _, v := range charCounts {
		if v > maxCount {
			maxCount = v
		}
		if v < minCount {
			minCount = v
		}
	}
	return maxCount - minCount
}

func pairInsertionOptimized(polymer string, rules map[string]rune, steps int) int {
	patternMapping := make(map[string]int)
	polymer = "#" + polymer + "#"
	for i := 0; i < len(polymer)-1; i++ {
		if _, ok := patternMapping[polymer[i:i+2]]; ok {
			patternMapping[polymer[i:i+2]]++
		} else {
			patternMapping[polymer[i:i+2]] = 1
		}
	}
	for i := 0; i < steps; i++ {
		newPatternMapping := make(map[string]int)
		for k, v := range patternMapping {
			if v < 1 {
				continue
			}
			if _, ok := rules[k]; !ok {
				if _, ok := newPatternMapping[k]; !ok {
					newPatternMapping[k] = v
				} else {
					newPatternMapping[k] += v
				}
				continue
			}
			insertion := rules[k]
			leftHalf := string(k[0]) + string(insertion)
			if _, ok := newPatternMapping[leftHalf]; ok {
				newPatternMapping[leftHalf] += v
			} else {
				newPatternMapping[leftHalf] = v
			}
			rightHalf := string(insertion) + string(k[1])
			if _, ok := newPatternMapping[rightHalf]; ok {
				newPatternMapping[rightHalf] += v
			} else {
				newPatternMapping[rightHalf] = v
			}
		}
		patternMapping = newPatternMapping
	}
	charCounts := make(map[rune]int)
	for k, v := range patternMapping {
		if _, ok := charCounts[rune(k[0])]; ok {
			charCounts[rune(k[0])] += v
		} else {
			charCounts[rune(k[0])] = v
		}
		if _, ok := charCounts[rune(k[1])]; ok {
			charCounts[rune(k[1])] += v
		} else {
			charCounts[rune(k[1])] = v
		}
	}
	delete(charCounts, '#')
	maxCount := 0
	minCount := math.MaxInt
	for _, v := range charCounts {
		if v > maxCount {
			maxCount = v
		}
		if v < minCount {
			minCount = v
		}
	}
	return (maxCount - minCount) / 2
}

func main() {
	polymer, rules, err := getInputs("input.txt")
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(pairInsertion(polymer, rules, 10))
	fmt.Println(pairInsertionOptimized(polymer, rules, 40))
}
