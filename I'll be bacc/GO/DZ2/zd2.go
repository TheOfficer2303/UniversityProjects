package main

import (
	"encoding/json"
	"log"
	"net/http"
	"net/url"
	"strconv"
	"strings"

	//"strconv"
	//"strings"
)
type webResponseAdd struct {
	Number1 int `json:"n1"` // input number1
	Number2 int `json:"n2"` // input number2
	Result int `json:"r"` // result of number1 + number2
}
func main() {
	http.HandleFunc("/add/", add)
	http.ListenAndServe(":8080", nil)
}

func add(w http.ResponseWriter, r *http.Request) {
	var a webResponseAdd

	path, _ := url.Parse(string(r.URL.RequestURI()))
	//log.Println(path)
	q := path.Query()

	if len(q) != 2 {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	log.Println(q)

	keys := make([]string, 0, len(q))
	for k := range q {
		keys = append(keys, k)
	}
	log.Println(keys)


	numberOneString := strings.Join(q[keys[0]], "")
	numberTwoString := strings.Join(q[keys[1]], "")

	//log.Print(numberOneString, numberTwoString)

	number1, _ := strconv.Atoi(numberOneString)
	number2, _ := strconv.Atoi(numberTwoString)
	//log.Print(number1, number2)
	result := number1 + number2


	a.Number1 = number1
	a.Number2 = number2
	a.Result = result

	jsonResponse, err := json.Marshal(a)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")

	if len(q) == 2 {
		_, _ = w.Write(jsonResponse)
	}

}