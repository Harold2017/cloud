package main

import "fmt"

// implement generator by closure
func fibonacciClosure() func() (ret int) {
	a, b := 0, 1
	return func() (ret int) {
		ret = b
		a, b = b, a + b
		return
	}
}

// implement generator by channel
func fibonacciChan(n int) chan int {
	ret := make(chan int)

	go func(){
		defer close(ret)
		a, b := 0, 1
		for i:=0; i<n; i++ {
			ret <- b
			a, b = b, a + b
		}
		// close(ret)
	}()
	return ret
}

func main() {
	// closure
	f := fibonacciClosure()
	for i:=0; i<20; i++ {
		fmt.Println(f())
	}

	// channel
	for i := range fibonacciChan(20) {
		fmt.Println(i)
	}
}
