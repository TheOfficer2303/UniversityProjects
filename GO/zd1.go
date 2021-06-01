package main
import (
	"errors"
	"fmt"
)
var errNoData = errors.New("no data in list")
type ShopItem struct {
	Name string
	Price int
	Callory int64
	Quantity int
}

func s() {
	shopList := []ShopItem{

		{"Hosomaki Ginger", 54, 250, 1},
		{"Mlijecna cokolada", 8, 600, 3},
		{"Banana", 10, 150, 6},
		{"2", 10, 150, 6},
		{"3", 10, 150, 6},
		{"4", 10, 150, 6},

	}
	tCal := totalCallory(shopList)
	fmt.Println(tCal) // 2950
	best, err := mostHealthy(shopList)
	fmt.Println(best) // [{Banana 10 150 6}]
	fmt.Println(err) // nil
}
func totalCallory(shoppingList []ShopItem) (total int)  {
	total = 0
	for i := 0; i < len(shoppingList); i++ {
		total += int(shoppingList[i].Callory) * shoppingList[i].Quantity
	}
	return total
}

func mostHealthy(shoppingList []ShopItem) (items []ShopItem, err error) {
	if shoppingList == nil {
		return nil, errNoData
	} else if len(shoppingList) == 0 {
		return items, errNoData
	}
	minCallories := shoppingList[0].Callory
	items = append(items, shoppingList[0])

	for i := 1; i < len(shoppingList); i++ {
		if shoppingList[i].Callory < minCallories {
			items = make([]ShopItem, 0)
			minCallories = shoppingList[i].Callory
			items = append(items, shoppingList[i])
		} else if shoppingList[i].Callory == minCallories {
			items = append(items, shoppingList[i])
		}
	}

	return items, nil
}