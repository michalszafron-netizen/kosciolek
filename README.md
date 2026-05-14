# Demo · Nowy landing parafialny + panel administracyjny

Wersja pokazowa nowej strony i CMS-a dla **Parafii pw. Najświętszego Serca Pana Jezusa w Czerwionce-Leszczynach**.

Stylistyka: koncepcja „Wspólnotowa karta" — ciepły beż + bordo + miedź,
typografia Playfair Display + Lato.

To jest **demo wyłącznie UI** — kliknij się po wszystkich ekranach jak w
prawdziwej aplikacji. Backend, baza danych i logowanie zostaną dodane
w kolejnym etapie (jeśli klient się zdecyduje).

## Co jest w paczce

```
demo-parafia-v2/
├── index.html                 ← STRONA GŁÓWNA — zacznij tutaj
├── strony/
│   ├── historia.html          ← przykład podstrony (pełna historia parafii + timeline)
│   └── kontakt.html           ← przykład podstrony (kontakt + numery kont)
├── admin/
│   ├── login.html             ← ekran logowania panelu
│   ├── index.html             ← pulpit admina (statystyki + ostatnia aktywność)
│   ├── aktualnosci.html       ← lista aktualności z filtrami
│   ├── aktualnosci-edit.html  ← edytor wpisu (z drag & drop zdjęć)
│   ├── ogloszenia.html        ← edytor ogłoszeń parafialnych + eksport PDF/Word
│   ├── galeria.html           ← lista galerii w siatce kart
│   ├── intencje.html          ← kalendarz tygodniowy intencji mszalnych
│   ├── ustawienia.html        ← ustawienia parafii (dane, konta, godziny)
│   └── assets/admin.css       ← współdzielony CSS panelu
├── public/
│   └── img/                   ← realne zdjęcia z parafii (wypełniane przez build.py)
├── build.py                   ← skrypt kopiujący zdjęcia z folderu Kosciol/
└── README.md                  ← ten plik
```

## Uruchomienie demo (2 minuty)

**Krok 1 — wypełnienie zdjęć.**
Otwórz CMD/PowerShell w folderze `demo-parafia-v2` i uruchom:

```cmd
python build.py
```

Skrypt skopiuje ~18 prawdziwych zdjęć z parafii (z folderu `Kosciol/content/galeria/`)
do `public/img/`. Bez tego kroku landing wyświetli się z pustymi polami obrazków.

**Krok 2 — otwarcie demo.**
Klikij dwukrotnie na `index.html` — otworzy się w przeglądarce. Albo:

```cmd
python -m http.server 8765
```

i wejdź na http://localhost:8765 (zalecane, niektóre przeglądarki mają
ograniczenia przy `file://`).

Jeśli ten port też jest zajęty, podstaw byle jaką inną liczbę z zakresu
**8000–9999**, np. `python -m http.server 4321`, i otwórz
`http://localhost:4321`.

**Krok 3 — kliknij po wszystkim.**
- Z landingu kliknij **„Panel parafii"** w prawym górnym rogu → trafisz na ekran logowania
- Na ekranie logowania kliknij **„Zaloguj się"** (login i hasło są wpisane — nie sprawdza)
- W panelu klikaj po menu po lewej: Pulpit / Aktualności / Ogłoszenia / Galeria / Intencje / Ustawienia
- Z listy aktualności kliknij **„Edytuj"** żeby zobaczyć pełny edytor wpisu
- Wróć na stronę z linkiem „Zobacz stronę" w pulpicie

## Co warto pokazać klientowi w pierwszej kolejności

1. **Hero z prawdziwymi zdjęciami parafii** (slider z 100-lecia)
2. **„Pigułki informacyjne"** — najbliższa msza, wydarzenie, kancelaria, intencja
3. **Karta ogłoszeń duszpasterskich** (lewa, bordo) — z eksportem PDF
4. **Galeria w stylu magazynowym** — niesymetryczna siatka
5. **Banner „Budujemy z Sercem"** — najważniejsza inwestycja parafii
6. **Sekcja historia + timeline** (klik na „Czytaj pełną historię")
7. **Panel admina → Intencje mszalne** — kalendarz tygodniowy z pustymi slotami i przyciskiem „Generuj PDF do druku" (to bolączka księdza)
8. **Panel admina → Edycja aktualności** — drag & drop zdjęć, edytor WYSIWYG

## Co działa, a co tylko wygląda

Działa (klikalne):
- Cała nawigacja między stronami i panelem
- Slider w hero (auto + kliknięcie kropek)
- Menu mobilne (responsywność)
- Logowanie → przejście do dashboardu

Tylko wygląda (UI mock):
- Wszystkie formularze (zapis, publikacja, eksport PDF/Word)
- Drag & drop zdjęć
- Statystyki w pulpicie (liczby są wstawione przykładowo)
- Wyszukiwanie

Tak wygląda specyfikacja UI/UX dla developera. Backend (Astro + Express +
SQLite na VPS-ie) buduje się dopiero po akceptacji wizualnej i podpisie
umowy.

## Co dalej

Po akceptacji wizualnej:
1. Postawienie środowiska na VPS-ie (Ubuntu + Nginx + PM2 + Let's Encrypt)
2. Budowa backendu Express + SQLite (~3–4 tygodnie)
3. Podpięcie panelu Decap CMS lub własny lekki admin Express
4. Migracja treści ze starej strony (już mamy oczyszczone teksty + 244 zdjęcia)
5. Szkolenie dla księdza (1–2 godz., zdalnie)
6. Wdrożenie i uruchomienie pod docelową domeną

## Kontakt

Demo przygotował: **Marek** · próbny landing parafialny dla **Michała**
Wersja: 14.05.2026 · koncepcja 2 — „Wspólnotowa karta"
