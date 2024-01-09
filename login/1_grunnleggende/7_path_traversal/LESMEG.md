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
* <https://en.wikipedia.org/wiki/Urlencoding>
