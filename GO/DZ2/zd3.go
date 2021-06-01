package main

import (
	"errors"
	"fmt"
	"sort"
	"time"
)

var (
	errNoData  = errors.New("no data")
	errTimeout = errors.New("timeout")
)

func sendData(numbers chan int) {
	num := []int{1, 2, 3, 4, 5, 1, 2, 3, 1}
	for _, v := range num {
		numbers <- v
	}
	close(numbers)
}

func main() {
	num := make(chan int, 1)
	go sendData(num)
	mostCommon, err := minFromChann(num)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(mostCommon)
	}
}

func minFromChann(numbers chan int) (int, error) {
	jmbagNumber := 942

	//_, ok := <- numbers
	//
	//if !ok && len(numbers) == 0 {
	//	return 0, errNoData
	//}

	var newNumbers []int

OUT:
	for  {
		select {
		case number, ok1 := <- numbers:
			if !ok1 {
				break OUT
			}
			newNumbers = append(newNumbers, number)
		case <- time.After(1 * time.Second):
			return 0, errTimeout
		}
	}

	if len(newNumbers) == 0 {
		return 0, errNoData
	}

	sort.Ints(newNumbers)
	min := newNumbers[0]

	return min * jmbagNumber, nil
}