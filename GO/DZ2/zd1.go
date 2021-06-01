package main

import (
	"errors"
	"fmt"
)

var errHighCalorieFood = errors.New("high calorie food not allowed")
type ShopItem struct {
	Name string
	Price int
	Callory int64
	Quantity int
}
func sendData1(shopItems chan ShopItem) {
	shopList := []ShopItem{
		{"Hosomaki Ginger", 54, 250, 1},
		{"Mlijecna cokolada", 8, 600, 3}, // ako se otkomentira ispisuje grešku
		{
			Name: "Banana",
			Price: 10,
			Callory: 150,
			Quantity: 6,
		},
	}
	for _, item := range shopList {
		shopItems <- item
	}
	close(shopItems)
}
func main() {
	num := make(chan ShopItem, 1)
	go sendData1(num)
	mostCommon, err := totalCost(300, num)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println("Total cost is", mostCommon) // rezultat primjera: mostCommon = 114
	}
}
func totalCost(maxCalorie int64, numbers chan ShopItem) (int, error) {
	total := 0
	for elem := range numbers {
		total += elem.Price * elem.Quantity
		if (elem.Callory > maxCalorie) {
			return 0, errHighCalorieFood
		}
	}
	return total, nil
}