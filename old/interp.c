#include <stdlib.h>
#include <stdio.h>

/*

SILLY

prim =
| int
| bool
| char
| list

expr =
| prim
| 





*/

double expression(void);

double vars[26]; // variables

char get(void) { 
    char c = getchar(); return c; 
} // get one byte

char peek(void) {
    char c = getchar(); ungetc(c, stdin); return c;
} // peek at next byte

double number(void) {
    double d; scanf("%lf", &d); return d; 
} // read one double

void expect(char c) { // expect char c from stream
    char d = get();
    if (c != d) {
        fprintf(stderr, "Error: Expected %c but got %c.\n", c, d);
    }
}

double expression(void) { // read an expression
    double e = term();
    while (peek() == '+' || peek() == '-') { // + or - more terms
        char c = get();
        if (c == '+') {
            e = e + term();
        } else {
            e = e - term();
        }
    }
    return e;
}

double read_statement(void) { // read a statement
    double ret;
    char c = peek();
    if (c >= 'A' && c <= 'Z') { // variable ?
        expect(c);
        if (peek() == '=') { // assignment ?
            expect('=');
            double val = expression();
            vars[c - 'A'] = val;
            ret = val;
        } else {
            ungetc(c, stdin);
            ret = expression();
        }
    } else {
        ret = expression();
    }
    expect('\n');
    return ret;
}

int main(void) {
    printf("> "); fflush(stdout);

    for (;;) {
        double v = read_statement();
        printf(" = %lf\n> ", v); fflush(stdout);
    }
    return EXIT_SUCCESS;
}