# wykop-obserwator-tagu

### Co to za program?
![Obrazek](https://i.imgur.com/XFn4OCr.png)

Obserwator tagu pozwala w czasie rzeczywistym śledzić podany tag w serwisie wykop.pl

### Wymagania do odpalenia

Testowałem kod jedynie na ubuntu 20.04 LTS. Do działania potrzebny jest `python3` oraz zainstalowanie bibliotek z `requirements.txt`
```
pip3 install -r requirements.txt
```

Ze względu na to, że program jest przystosowany do uruchamiania lokalnego potrzebne są klucze api.
Można je wygenerować [tutaj](https://www.wykop.pl/dla-programistow/nowa-aplikacja/).

Program wczytuje je z dwóch zmiennych środowiskowych:
* `WYKOP_TAG_KEY` - klucz
* `WYKOP_TAG_SECRET` - sekret


### Instrukcja odpalenia

```
usage: main.py [-h] [-i INTERVAL] [-n MESSAGES_NUMBER] [--no-images] tag

positional arguments:
  tag                 Watched tag

optional arguments:
  -h, --help          show this help message and exit
  -i INTERVAL         How often try to download new messages from wykop api
                      [in seconds]
  -n MESSAGES_NUMBER  How many recent messages are downloaded each time
  --no-images         Do not convert images into ascii images
```

### Jak można kontrybuowac

1. Zgłosić problem do [issues](https://github.com/krasnoludkolo/wykop-obserwator-tagu/issues) (staram się je od razu sprawdzać)
2. Zrobić forka repo, wprowadzić zmiany i wystawić PR. Jeśli byłaby to implementacja istniejącego [issue](https://github.com/krasnoludkolo/wykop-obserwator-tagu/issues) warto napisać w komentarzu, że się nad nim pracuje. Najlepiej też oznaczyć mnie w PR.

### Jak można wspomóc autora ( ͡° ͜ʖ ͡°)
Napisz do mnie na PW na wykopie, dogadamy się: [krasnoludkolo](https://www.wykop.pl/ludzie/krasnoludkolo/)
Ewentualnie na maila: [janek@projmen.pl](mailto:janek@projmen.pl)
