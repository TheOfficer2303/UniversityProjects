package main

import (
	"fmt"
	"reflect"
	"unicode"
)
type Point struct {
	X int
	Y int
	private string
}
func main() {
	fmt.Println(fields(Point{})) // [X Y]
}
func fields(t interface{}) []string {
	exportedFields := make([]string, 0)
	fmt.Println(exportedFields)

	e := reflect.ValueOf(t)

	for i := 0; i < e.NumField(); i++ {
		name := e.Type().Field(i).Name

		fmt.Println(name)

		if unicode.IsUpper([]rune(name)[0]) {
			exportedFields = append(exportedFields, name)
		}

	}

	return exportedFields
}

