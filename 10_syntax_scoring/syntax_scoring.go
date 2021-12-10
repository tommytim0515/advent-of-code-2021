package main

import (
	"fmt"
	"os"
	"sort"
	"strings"
)

var setNotations = []rune{')', ']', '}', '>'}
var notationMapping = map[rune]rune{
	'(': ')',
	'[': ']',
	'{': '}',
	'<': '>',
	')': '(',
	']': '[',
	'}': '{',
	'>': '<',
}
var wrongNotationScoreMapping = map[rune]int{
	')': 3,
	']': 57,
	'}': 1197,
	'>': 25137,
}
var completeScoreMapping = map[rune]int{
	')': 1,
	']': 2,
	'}': 3,
	'>': 4,
}

func getInputs(filename string) ([]string, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	return strings.Split(string(data), "\n"), nil
}

func intersection(a, b []rune) []rune {
	m := make(map[rune]bool)
	for _, v := range a {
		m[v] = true
	}
	var result []rune
	for _, v := range b {
		if checked, ok := m[v]; ok {
			if checked {
				result = append(result, v)
				m[v] = false
			}
		}
	}
	return result
}

func syntaxErrScore(lines []string) int {
	var score int
	for _, line := range lines {
		var stack []rune
		for _, char := range line {
			if char == '(' || char == '[' || char == '{' || char == '<' {
				stack = append(stack, char)
				continue
			}
			if len(stack) > 0 && stack[len(stack)-1] == notationMapping[char] {
				stack = stack[:len(stack)-1]
			} else {
				stack = append(stack, char)
			}
		}
		if len(stack) == 0 {
			continue
		}
		wrongNotations := intersection(stack, setNotations)
		if len(wrongNotations) == 0 {
			continue
		}
		var wrongNotation rune
		minIdx := len(stack)
		for _, notation := range wrongNotations {
			if idx := strings.IndexRune(string(stack), notation); idx < minIdx {
				fmt.Println(idx)
				minIdx = idx
				wrongNotation = notation
			}
		}
		score += wrongNotationScoreMapping[wrongNotation]
	}
	return score
}

func fixIncomplete(lines []string) int {
	var scores []int
	for _, line := range lines {
		var stack []rune
		for _, char := range line {
			if char == '(' || char == '[' || char == '{' || char == '<' {
				stack = append(stack, char)
				continue
			}
			if len(stack) > 0 && stack[len(stack)-1] == notationMapping[char] {
				stack = stack[:len(stack)-1]
			} else {
				stack = append(stack, char)
			}
		}
		if len(stack) == 0 {
			continue
		}
		wrongNotations := intersection(stack, setNotations)
		if len(wrongNotations) != 0 {
			continue
		}
		var addition []rune
		for i := len(stack) - 1; i >= 0; i-- {
			addition = append(addition, rune(notationMapping[stack[i]]))
		}
		var score int
		for _, char := range addition {
			score *= 5
			score += completeScoreMapping[char]
		}
		scores = append(scores, score)
	}
	sort.Ints(scores)
	if len(scores)%2 == 0 {
		return (scores[len(scores)/2] + scores[len(scores)/2-1]) / 2
	}
	return scores[len(scores)/2]
}

func main() {
	inputs, err := getInputs("input.txt")
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("Err score: %d\n", syntaxErrScore(inputs))
	fmt.Println("Incomplete score:", fixIncomplete(inputs))
}
