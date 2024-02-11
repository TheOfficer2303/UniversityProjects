package main

import "fergo.dev/H9/shapes"

type Octagon struct{}

func (d *Octagon) NumberOfSides() int {
	return 8
}

func (d *Octagon) Type() string {
	return "octagon"
}


func countSides(shapes []shapes.GeometricShape) int {
	numberOfSides := 0

	for _, shape := range shapes {
		numberOfSides += shape.NumberOfSides()
	}

	return numberOfSides
}
