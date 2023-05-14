grammar lc;

root : terme ;

terme :  '(' terme ')'              # parentesis
    | terme terme                   # aplicacio
    | LAMBDA LLETRA+ '.' terme      # abstraccio
    | LLETRA                        # lletra
    ;

LLETRA : [a-z] ;

LAMBDA : 'λ' | '\u005C' ;

WS : [ \t\n\r]+ -> skip ;