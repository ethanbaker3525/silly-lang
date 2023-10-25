#include <regex.h>
#include <stdio.h>
#include "toks.h"


int init_tok_ref(regex_t *tok_ref) {

    /* adding toks */
    regcomp(&tok_ref[TOK_COMMENT],  REG_COMMENT,   REG_EXTENDED);
    regcomp(&tok_ref[TOK_INT],      REG_INT,       REG_EXTENDED);
    regcomp(&tok_ref[TOK_ADD],      REG_ADD,       REG_EXTENDED);
    regcomp(&tok_ref[TOK_SUB],      REG_SUB,       REG_EXTENDED);
    regcomp(&tok_ref[TOK_MUL],      REG_MUL,       REG_EXTENDED);
    regcomp(&tok_ref[TOK_DIV],      REG_DIV,       REG_EXTENDED);
    return 0;

}

int free_tok_ref(regex_t *tok_ref) {

    for (int i = 0; i < NUM_TOKS; i++) {

        regfree(&tok_ref[i]);

    }

}

struct tok *newTok(int type, char *match, regmatch_t pmatch) {

    Tok *t = malloc(sizeof(Tok));
    t.type = type;
    t.value = malloc() // stopped here, jesus c is hard


}

void freeTok(Tok *tok) {


}