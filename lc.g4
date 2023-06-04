grammar lc;

root : instruccio+ ;

instruccio: VAR EQ terme            # assignacio
    | terme                         # expressio
    ;

terme :  '(' terme ')'              # parentesis
    | terme terme                   # aplicacio
    | LAMBDA LLETRA+ '.' terme      # abstraccio
    | VAR                           # variable
    | LLETRA                        # lletra
    ;

EQ : '≡' | '=' ;

LLETRA : [a-z] ;

VAR: ([A-Z] ([A-Z] | [0-9])*) | SYMBOL;
SYMBOL: ( [\u0021-\u0027] | [\u002A-\u002D] | [\u002F] | [\u003A-\u003C] | [\u003E-\u0040] | [\u005B] | [\u005D-\u0060] | [\u007B-\u007E] | [\u00A0-\u00AC] | [\u00AE-\u00EF] | [\u00F7] ) ;
LAMBDA : 'λ' | '\u005C' ;

WS : [ \t\n\r]+ -> skip ;