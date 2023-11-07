#include <stdio.h>
#include <regex.h>
#include <string.h>

#include "toks.h"
#include "lexer.h"

*Tok match_tok(regex_t *tok_ref, Tok *tok, char *str) {

    int match;
    int status;
    regmatch_t  pmatch[2]; // one extra capture group
    
    for (int type = 0; type < NUM_TOKS; type++) {

        if (!regexec(&tok_ref[type], str, 2, pmatch, 0)) {
            
            //str[pmatch[1].rm_eo] = '\0';
            Tok t = {type, str + pmatch[1].rm_so};
            printf("%d\n", pmatch[1].rm_so);
            printf("%d\n", pmatch[1].rm_eo);
            return t;

        }

    }

    *tok = {-1, NULL};
    return t;

}

Tok *tokenize(FILE *stream) { /* tokenize input into descrete toks */

    char read[MAX_TOK_LEN];
    int value;

    /*while (fgets(read, MAX_TOK_LEN, stream)) {

        value = regexec(&re, read, 0, NULL, 0);
        printf("%d\n", value);

    }*/

}

int main(void) {

    regex_t tok_ref[NUM_TOKS] = {0};
    init_toks(tok_ref);

    char *test = "  + #21ewe3";

    Tok first = match_tok(tok_ref, test);

    //test = test + 6;

    printf("%d\n", first.type);
    printf("%s\n", first.value);
    //free_toks(tok_ref);

}