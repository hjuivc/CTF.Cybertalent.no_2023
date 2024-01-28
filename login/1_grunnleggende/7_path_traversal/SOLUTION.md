# Path traversal

  

Når en bruker selv kan påvirke hvilket filnavn et program skal jobbe med, kan det åpne for sårbarheter av typen *path traversal* eller *path manipulation*. I denne katalogen finner du et program som lar deg lese elektroniske bøker: `./les_bok`. Du har selv ikke tilgang til å åpne bok-filene som er lagret i underkatalogen `bok/`. Programmet derimot har rettigheter til å lese filene -- og *flaggene* :)

Se om du kan få tilgang til bok-filene og flaggene da vel! Du kan kikke i kildekoden til programmet: `les_bok.c`. Denne oppgaven har flere løsninger.

```sh
$ cat les_bok.c
$ ./les_bok
$ ./les_bok frankenstein
$ ./les_bok FLAGG.txt
$ ???
$ scoreboard <FLAGG>
```

Linker:
* <https://owasp.org/www-community/attacks/Path_Traversal>
* <https://en.wikipedia.org/wiki/Urlencoding

# Solution

Da jeg utforsket Path Traversal-oppgaven og la merke til at `les_bok`-programmet automatisk la til `.txt` til filnavnene jeg oppga, bestemte jeg meg for å prøve en annen tilnærming. Hver gang jeg prøvde en Path Traversal-kommando, endte jeg opp med feilmeldinger som "No such file or directory" fordi programmet prøvde å åpne filer som `bok/BONUS_FLAGG.txt.txt`. Derfor tenkte jeg å fjerne `.txt` fra kommandoen min. Jeg prøvde `./les_bok ../FLAGG`, og til min overraskelse fungerte det! Programmet la til `.txt` selv og åpnet `FLAGG.txt`-filen jeg prøvde å nå.

```sh
login@corax:~/1_grunnleggende/7_path_traversal$ ./les_bok ../FLAGG
```

![[Pasted image 20240115195609.png]]

```sh
login@corax:~/1_grunnleggende/7_path_traversal$ scoreboard c1b59bdd13b7ad853bb623d672c51234
Kategori: 1. Grunnleggende
Oppgave:  1.7_path_traversal
Svar:     c1b59bdd13b7ad853bb623d672c51234
Poeng:    10

Gratulerer, korrekt svar!
```


### Bonus flagg:
lik løste jeg oppgaven med path traversal og fant flagget:

1. Jeg startet med å utforske programmet `./les_bok` og innså at det tillot meg å lese bøker fra underkatalogen `bok/`, men jeg manglet tilgang til `BONUS_FLAGG`.
    
2. Jeg så på kildekoden `les_bok.c`, men fant ingen åpenbar måte å lese `BONUS_FLAGG` direkte uten `.txt`-utvidelsen.
    
3. Jeg husket at null bytes `%00` kan injiseres for å avslutte filnavn. For eksempel: `?file=secret.doc%00.pdf` ville gi en fil som slutter på `.doc`, men operativsystemet ser det som `.pdf`.
    
4. Jeg brukte denne teknikken ved å kjøre kommandoen: `./les_bok ../BONUS_FLAGG%00`.
    
5. Resultatet var at programmet behandlet filen som `BONUS_FLAGG` uten `.txt`-utvidelsen, og jeg fikk tilgang til flagget.

På denne måten kunne jeg omgå begrensningene og lese `BONUS_FLAGG`.
![[Pasted image 20240115203346.png]]
```sh
login@corax:~/1_grunnleggende/7_path_traversal$ ./les_bok ../BONUS_FLAGG%00
login@corax:~/1_grunnleggende/7_path_traversal$ scoreboard bc7f37bf13b7773cc361e002bc5ab7b0
Kategori: 1. Grunnleggende
Oppgave:  1.8_path_traversal_bonus
Svar:     bc7f37bf13b7773cc361e002bc5ab7b0
Poeng:    10

Gratulerer, korrekt svar!
```