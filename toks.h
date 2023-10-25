#define NUM_TOKS 6

#define TOK_COMMENT 0
#define REG_COMMENT "^[ \t\n\r\f\v]*#(.*)"

#define TOK_INT     1
#define REG_INT     "^[ \t\n\r\f\v]*(\\d+)"

#define TOK_ADD     2
#define REG_ADD     "^[ \t\n\r\f\v]*(\\+)"

#define TOK_SUB     3
#define REG_SUB     "^[ \t\n\r\f\v]*(-)"

#define TOK_MUL     4
#define REG_MUL     "^[ \t\n\r\f\v]*(\\*)"

#define TOK_DIV     5
#define REG_DIV     "^[ \t\n\r\f\v]*(/)"

typedef struct tok {

    int type;
    void *value;

} Tok;

int init_toks(regex_t *tok_ref);
int free_toks(regex_t *tok_ref);


