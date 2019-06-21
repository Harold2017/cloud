// reference: https://stackoverflow.com/questions/51183462/how-to-copy-os-stdout-output-to-string-variable

package main

import (
	"fmt"
	"io"
	"os"
	"strings"
)

// capture replaces os.Stdout with a writer that buffers any data written 
// to os.Stdout. Call the returned function to cleanup and get the data
// as a string.
func capture() func() (string, error) {
    r, w, err := os.Pipe()
    if err != nil {
        panic(err)
    }

    done := make(chan error, 1)

    save := os.Stdout
    os.Stdout = w

    var buf strings.Builder

    go func() {
        _, err := io.Copy(&buf, r)
        r.Close()
        done <- err
    }()

    return func() (string, error) {
        os.Stdout = save
        w.Close()
        err := <-done
        return buf.String(), err
    }
}

func main() {
	done := capture()
	fmt.Println("Hello World!")
	capturedOutput, err := done()
	if err != nil {
		fmt.Println("Error: ", err.Error())
	} else {
		fmt.Println("Captured: ", capturedOutput)
	}
}
