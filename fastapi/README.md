# Timinis egen FastAPI

Vi bruker FastAPI som har en grundig dokumentasjon [her](https://fastapi.tiangolo.com/)
**Merk: Selv om typedeklarasjoner ikke faktisk betyr noe i python, er FastAPI strenge på det, og vil validere mhp typehint. BRUK DEM**

## Dev-Ops

For å utvikle i et større samarbeidsprosjekt er det lurt å opprettholde noen kodekvalitets-normer som gjør koden både leselig og strukturelt standardisert. I tillegg er det greit å har erfaring med hvordan python-kode *bør* se ut ifølge stil-guiden [PEP8](https://peps.python.org/pep-0008/), som gjerne følges ute i det store arbeidsliv.

Først er det lurt at alle som utvikler bruker det samme utviklingsmiljø (samme environment). Rent kodekjøringsmessig har ikke dette utrolig mye å si her, siden koden uansett kjøres i et docker-bilde som er ferdigdefinert i dette repoet (slik jeg forstår det ihvertfall, @iverks rett på meg), men det er greit å ha siden det bare ordner all installasjon av dependencies for blant annet kodekvalitets-sjekkere.

### Poetry
Poetry er et utviklingsverktøy som forsikrer og håndterer dependencies i Python-prosjekter, og setter rimelig automatisk opp en Python-installasjon som har nøyaktig det som trengs for å utvikle i dette repository-et. For installasjon, se [her](https://python-poetry.org/docs/).

For å bruke Poetry i konsoll/terminal er det greit å ha filstien til poetry.exe inn i `path` i PC-ens miljøvariabler. Når dette er fiksa (kan kreve reboot) kan man sjekke at installasjonen er ok ved å kjøre følgende i konsoll:

```console
C:\Users\USER> cd C:\path-to-repo\timini-fastapi
path-to-repo\timini-fastapi> Poetry
Poetry version 1.1.14
...
```

Deretter kan man installere Pythonprosjekt-miljøet ved å kjøre

```console
Poetry env use "path-to-python3.10\python.exe"
Poetry install
Poetry shell
```
Sistnevnte gjør at du lager et konsollvindu som bruker miljøet definert av innholdet i pyproject.toml. Da kan du også enkelt kjøre pre-commit fra konsoll.

### Pre-commit

Pre-commit kjører kodekvalitets-sjekker på koden din, you guessed it, før du committer kode til git, i steget mellom staging og commit. En typisk workflow for dette vil være

```console
git add -A
pre-commit
pre-commit run --all-files
```

som kjører kodekvalitets-tester på henholdsvis filene i staging area og alle filer i repoet. Kodekvalitetssjekkene er definert i .pre-commit-config.yaml. Sjekkene gir tilbakemeldinger og retter i mange tilfeller opp i formatteringsfeil for deg (dog ikke alle).

## Docker

Størsteparten av kommandoene gitt her skal kjøres inne i docker containeren. For å gå inn i den kan man enten bruke dockers egen GUI eller å kjøre kommandoen: `docker exec -it timini-fastapi-backend-1 /bin/bash`, som åpner bash i containeren. For å forlate skriv `exit`

## For å kjøre koden utenom docker

`uvicorn main:app --reload`

## OpenAPI

Med FastAPI følger OpenAPI, det vil si at API'en dokumenterer seg selv. Dokumentasjonen kan du finne her:
[swagger docs](http://127.0.0.1:8000/docs)
[alternaltiv docs](http://127.0.0.1:8000/redoc)
'
TODO: `https://auth0.com/docs/security/tokens/refresh-tokens/refresh-token-rotation`

## Alembic

**Kommentar: vi bruker ikke alembic nå fordi vi bruker SQLModel som ikke har dokumentasjon for hvordan man bruker det med alembic. [Så fort dokumentasjonen kommer](https://sqlmodel.tiangolo.com/advanced/) så må det fikses.**

Vi bruker alembic for migrations. Du må installere alembic på din egen pc for at migrasjonsskriptene skal komme på git. Det gjør du ved `pip install alembic` eller `pip install -r requirements.txt`. Siste alternaltiv gir deg alt av andre plugins også, som er fint for code completion.

<!-- Det går kanskje an å generere fra inne i docker men jeg fikk det ikke til å funke --iverks  -->

For å generere et skript skriver du i din egen terminal (i timini-fastapi mappen) `alembic revision --autogenerate -m <hva gjør skriptet>`.
For å kjøre skriptet går du inn i docker containeren som forklart tidligere og kjører `alembic upgrade head`. Her betyr head "nyeste versjon". Du kan også spesifisere en versjon med den rare strengen før understreken i filnavnet.

## Testing

Jeg implementerte testing fordi det gjorde utviklingen av kjernen mye enklere, og gjorde at jeg kunne være sikker på at tabellene og forholdene mellom de oppførte seg som det skulle.
Om testing gjør at det blir vanskeligere for dere å utvikle trenger dere ikke å gjøre det, men jeg tror det kommer til å hjelpe. Jeg kunne ingenting om det før jeg begynte, og tutorialen under er mer en grundig nok men tar allikevel bare maks 30 min å lese. I mange tilfeller holder det å ha lest [denne (som tar kanskje 5min.)](https://fastapi.tiangolo.com/tutorial/testing/)
Vi bruker pytest og FastApis(starlettes) testclient for testing. [Du kan lese om det her](https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/).
