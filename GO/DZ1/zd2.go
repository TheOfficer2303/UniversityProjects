package main
import (
	"fmt"
	"strings"
)

func d() {
	numbers := "Lorem ipsum dolor sit amet"
	num, occurrence := countWords(numbers)
	fmt.Println(num, occurrence) // 5 map[amet:1 dolor:1 ipsum:1 lorem:1 sit:1]
}
func countWords(sentence string) (int, map[string]int) {
	sentence = strings.ReplaceAll(sentence, ",", "")
	sentence = strings.ReplaceAll(sentence, ".", "")

	splitted := strings.Fields(sentence)

	for i := 0; i < len(splitted); i++ {
		splitted[i] = strings.ToLower(splitted[i])
	}


	words := make(map[string]int)
	for _, word := range splitted {
		_, matched := words[word]
		if matched {
			words[word] += 1
		} else {
			words[word] = 1
		}
	}
	num := len(words)

	return num, words

}