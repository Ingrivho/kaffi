# proglab2

## Tentativ arbeidsfordeling

Mathilde tar seg av sensobs, Rasmus tar seg av behaviors og Gorm tar seg av arbitrator og motob. 

Forslag, muligens ukloks: Lag debug-mode, hvor dummykode kommer inn og output printes. Det vil gjøre det lettere å sette alt sammen uten at programmet feiler på steder som er vanskelige å finne.

## Hvordan finne IPen og logge på Pien

http://folk.ntnu.no/haakongi/TDT4113/get_ip_from_mac.php

Søk etter b8:27:eb:a2:fd:46

Logg på Pien med "ssh root@[ip]" eller "ssh pi@[ip]". 

## Gorms guide til litt forskjellig
Jeg bruker en Windows-maskin, og Cmder som terminal-emulator.

### Start en webserver for å gjøre filer (som bildet fra kameraet) tilgjengelig via nettleser:

Kjør webserver.py på Pien og gå til Pien sin IP i nettleser på en annen maskin på samme nettverk. Alle filene i robot-mappen vil være tilgjengelige. Hvis du får permission denied er det fordi du ikke er root. Prøv "sudo python3 webserver.py".

### Git basics

* git clone https://github.com/Gggorm/robot.git: for å få ned remote repo til lokal maskin.
* git status: se om du har noen uncommitta filer f.eks.
* git add [filnavn]: legg til en ny fil så den trackes
* git commit -am "kommentar om hva du har endret": committer endringene (mappens tilstand blir da et save-punkt på din lokale maskin, som man kan gå tilbake til senere om det trengs)
* git push origin: send commit-savepunktet/tilstanden til remote repo på github.
* git pull: Hent ned og merge inn alt som er (på tilsvarende branch) på serveren. Dette går ikke hvis man har uncommitta endringer lokalt, så disse må enten committes eller ignoreres (se git checkout)
* git checkout .: Glem alle endringer som har blitt gjort men ikke committa.
* git diff: Få printet ut til konsoll alle endringer man har gjort i forhold til forrige commit.

### Noen kommandoer for å lettere jobbe i terminal

* cat [filnavn]: få innholdet i en fil printet til konsoll. Kommandonavnet kommer av concatenate, fordi det kan brukes til å sammensette en liste filer.
* less: en utility for å få pagination for lengre filer. Brukes gjerne i kombinasjon med cat, slik: "cat README.md | less". "|"-tegnet er en "pipe", som sender videre output fra en kommando slik at det blir input for en annen.
* pwd: Finn ut hvor du er i filsystemet. Navnet kommer av pathname of working directory
* mkdir [mappenavn]: Lag mappe
* touch [filnavn]: Lag fil
* rm [filnavn]: Slett fil
* rm -rf [mappenavn]: Slett mappe og alt innhold
* nano [filnavn]: Åpne fil i redigeringsverktøyet nano (som er installert på Pien, men ikke nødvendigvis ellers)
* vim [filnavn]: Åpne fil i vim. Noen steder er kun vi installert. Det er for viderekomne. Veldig lett å kludre ting til.
* cd
* ls

### Kopier filer fra en maskin til en annen med SCP-kommandoen:

Her står jeg i en mappe på min Windows-PC, og SCPer fra en remote mappe på Pien til en lokal (relativt adressert) mappe:

    c:\Google Drive\Skole\Proglab 2\robot (master)
    λ scp root@192.168.1.5:/home/pi/robot/image.png images/
    
For å kopiere mer enn enkeltfiler er nok git bedre, siden det blir en del rotefiler generert av IDEer og foreskjellige operativsystemer. Det er lett å fikse med git, ved å legge til oppføringer i .gitignore.


## Finns tips til resetting av IP

    sudo service networking force-reload
    
## Egenskaper Roar skal ha

1. Han skal stoppe før han kræsjer i vegger han kjører mot
2. Han skal ikke kjøre inn i vegger som er nærmere enn 3 cm fra han på høyre og venstre side
3. Han skal ikke kjøre over sorte linjer
4. Når har ser et rødt objekt (mål) så kjører han mot det. 