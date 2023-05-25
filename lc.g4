grammar lc;

root : instruccio+ ;

instruccio: VAR '≡' terme           # assignacio
    | terme                         # expressio
    ;

terme :  '(' terme ')'              # parentesis
    | terme terme                   # aplicacio
    | LAMBDA LLETRA+ '.' terme      # abstraccio
    | VAR                           # variable
    | LLETRA                        # lletra
    ;

LLETRA : [a-z] ;

VAR : [A-Z]+;

LAMBDA : 'λ' | '\u005C' ;

WS : [ \t\n\r]+ -> skip ;