package main

import (
	"fmt"
)

func main() {
	shapes := []GeometricShape{
		&Dot{},
		&Henagon{},
		&Digon{},
		&RightTriangle{},
		&RightTriangle{},
		&EquilateralTriangle{},
	}
	fmt.Println(countTriangles(shapes)) // 3
	fmt.Println(countPolygons(shapes))  // 5
}

func countTriangles(shapes []GeometricShape) int {
	number := 0

	for _, shape := range shapes {
		_, ok := shape.(Triangle)

		if ok {
			number += 1
		}

	}

	return number
}

func countPolygons(shapes []GeometricShape) int {
	number := 0

	for _, shape := range shapes {
		_, ok := shape.(Polygon)

		if ok {
			number += 1
		}

	}

	return number
}
