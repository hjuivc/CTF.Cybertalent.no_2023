# Reverse engineering

Enten du leter etter sårbarheter eller analyserer skadevare må du kunne plukke fra hverandre en programfil for å se hva den gjør, uten å ha tilgang til kildekode. Denne prosessen blir kalt *reverse engineering*, eller mer populært bare *reversing*. Å reverse større programmer krever mye tid og erfaring, og det tar lang tid å lære verktøyene til det fulle.

I lang tid har det beste verktøyet for reversing av programmer vært *IDA Pro*, og dette har nærmest vært en industristandard. I 2019 publiserte amerikanske *NSA* et internt verktøy de kaller *Ghidra*, som er gratis og åpen kildekode.

Det finnes også noen mer spesialiserte reversing verktøy, som `jadx` for android reversing.

Det er mulig å løse denne oppgaven med enkle verktøy som `strings` og `objdump`, men vi anbefaler å bruke *Ghidra* eller gratisversjonen av *IDA*.

For å kopiere filer ut fra denne serveren kan du bruke kommandoen `scp` fra **din egen maskin**: `scp login@ctf.cybertalent.no:1_grunnleggende/6_reversing/check_password ./check_password`

Hvordan løser **du** denne oppgaven?

Linker:

* [Ghidra](https://ghidra-sre.org/)
* [Presentasjon av Ghidra fra INFILTRATE 2019](https://vimeo.com/335158460)
* [IDA](https://www.hex-rays.com/products/ida/support/download.shtml)
* [Cutter](https://cutter.re/)
* [Binary ninja](https://binary.ninja/)
* [jadx](https://github.com/skylot/jadx)

# Solution

# Prosessen for Å Løse CTF-utfordringen med Ghidra

## 1. Åpne Filen i Ghidra
- **Start Ghidra:** Du begynte med å åpne Ghidra, et avansert verktøy for reverse engineering.
- **Importer filen:** Deretter importerte du den binære filen (som i dette tilfellet var `check_password`) inn i Ghidra for analyse.

## 2. Kjøre Analyse
- **Analyser den importerte filen:** Etter å ha importert filen, kjørte du Ghidras analysefunksjon. Dette er et kritisk steg da det lar Ghidra dekompilere binærfilen og oversette den til en mer lesbar form.
## 3. Navigering i Dekompilert Kode

- **Naviger til `main`-funksjonen:** I Ghidra's dekompilerte visning, navigerte du til `main`-funksjonen. Dette er ofte startpunktet for detaljert analyse ettersom `main` vanligvis inneholder den primære kjørelogikken for programmet.
- **Utforske koden:** Innen `main`, utforsket du hvordan programmet håndterer inndata, og hvilke funksjoner og betingelser som er involvert.
## 4. Dykke Inn i `check_password`

- **Finn og analyser `check_password`-funksjonen:** Etter å ha identifisert at `check_password`-funksjonen var nøkkelen til å forstå passordlogikken, navigerte du til denne funksjonen i Ghidra.
- **Bryt ned funksjonens logikk:** Innen `check_password`, analyserte du hvordan den prosesserer inndata og hva som kreves for at et passord skal godkjennes. Dette involverte å forstå de spesifikke strengsammenligningene og betingelsene i funksjonen.

## 5. Løse Passordet

- **Deduser passordet basert på analysen:** Basert på din grundige analyse av `check_password`, kunne du dedusere det korrekte passordet, `Reverse_engineering_er_morsomt__`.
- **Bekreftelse:** Til slutt bekreftet du løsningen ved å teste passordet direkte i programmet, noe som var vellykket.

![Alt text](Pasted%20image%2020240115192943.png)

## Konklusjon

- **Anvendelse av reverse engineering:** Denne prosessen demonstrerte hvordan reverse engineering kan brukes til å dekonstruere og forstå den interne logikken i et program, selv uten tilgang til kildekoden.
- **Tålmodighet og nøye analyse:** Løsningen krevde tålmodighet og en metodisk tilnærming for å navigere og analysere dekompilert kode i Ghidra.


Denne prosessen illustrerer trinnene og tankemåten bak reverse engineering med Ghidra, fra å åpne og analysere filen, til detaljert undersøkelse av funksjoner og til slutt å løse og verifisere passordet.

Levering av flagg:
```sh
FLAGG  LESMEG.md  check_password  check_password.c
login@corax:~/1_grunnleggende/6_reversing$ ./check_password
Bruk: ./check_password PASSORD

Sjekk passord gitt som første argument.
Hvis passordet er korrekt startes et nytt shell med utvidete rettigheter.
login@corax:~/1_grunnleggende/6_reversing$ ./check_password Reverse_engineering_re_mostrom_
Feil passord :(
Du stoppet på steg 1
login@corax:~/1_grunnleggende/6_reversing$ ./check_password Reverse_engineering_er_morsomt
Feil passord :(
Du stoppet på steg 1
login@corax:~/1_grunnleggende/6_reversing$ ./check_password Reverse_engineering_er_morsomt_
Feil passord :(
Du stoppet på steg 1
login@corax:~/1_grunnleggende/6_reversing$ ./check_password Reverse_engineering_re_mostrom_
Feil passord :(
Du stoppet på steg 1
login@corax:~/1_grunnleggende/6_reversing$ ./check_password Reverse_engineering_er_morsomt_
Feil passord :(
Du stoppet på steg 1
login@corax:~/1_grunnleggende/6_reversing$ ./check_password Reverse engineering er morsomt
Bruk: ./check_password PASSORD

Sjekk passord gitt som første argument.
Hvis passordet er korrekt startes et nytt shell med utvidete rettigheter.
login@corax:~/1_grunnleggende/6_reversing$ ./check_password Reverse_engineering_re_mostrom_
Feil passord :(
Du stoppet på steg 1
login@corax:~/1_grunnleggende/6_reversing$ ./check_password Reverse_engineeriing
Feil passord :(
Du stoppet på steg 1
login@corax:~/1_grunnleggende/6_reversing$ ./check_password Reverse_engineering
Feil passord :(
Du stoppet på steg 1
login@corax:~/1_grunnleggende/6_reversing$ ./check_password Reverse_engineering_er_morsomt__
Korrekt passord!

Videreført til nytt skjell:
$ ls
FLAGG  LESMEG.md  check_password  check_password.c
$ cat FLAGG
FLAGG: dfe3ab692162908657da84f938179245
$ scoreboard dfe3ab692162908657da84f938179245
Kategori: 1. Grunnleggende
Oppgave:  1.6_reversing
Svar:     dfe3ab692162908657da84f938179245
Poeng:    10

Gratulerer, korrekt svar!
```

