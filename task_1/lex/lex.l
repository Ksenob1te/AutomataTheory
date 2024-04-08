%option noyywrap
%x SERVER TAIL
%%
<INITIAL> {
^(?i:irc\:\/\/) BEGIN(SERVER);
\n return 0;
. ;
}
<SERVER> {
(?i:\w+) {BEGIN(END); return 1;}
. BEGIN(INITIAL);
\n {BEGIN(INITIAL); return 0;}
}
<TAIL> {
(?i:(\:(6553[0-5]|655[0-2][1-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[0-5][0-9]{4}|[0-9]{1,4}))?($|/(\w+)?(\?(\w+))?\n) {BEGIN(END); return 1;}
. BEGIN(INITIAL);
\n {BEGIN(INITIAL); return 0;}
}
<END> {
. ;
\n BEGIN(INITIAL);
}