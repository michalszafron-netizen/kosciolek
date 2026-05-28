# Handover — Demo Parafia NSPJ Czerwionka-Leszczyny

> **Dokument przekazania projektu dla kolejnego developera.**  
> Ostatnia aktualizacja: **2026-05-28**  
> Repo: `michalszafron-netizen/kosciolek`, branch `master`

---

## 1. Czym jest ten projekt

**Statyczne demo HTML/CSS/JS** — landing page + kompletny panel administracyjny CMS dla Parafii pw. Najświętszego Serca Pana Jezusa w Czerwionce-Leszczynach.

**Brak backendu.** Cały stan aplikacji przechowywany w `localStorage` przeglądarki. Po akceptacji UI powstanie właściwy backend: Astro + Express + SQLite na VPS.

Stylistyka: koncepcja „Wspólnotowa karta" — ciepły beż (`#f4ede0`) + bordo (`#7a1f2b`) + miedź (`#b87a4a`), typografia Playfair Display + Inter.

```bash
# Uruchomienie lokalne
cd demo-parafia-v2
python -m http.server 8765
# → http://localhost:8765
```

---

## 2. Aktualna struktura plików

```
demo-parafia-v2/
├── index.html                  ← STRONA GŁÓWNA
├── strony/
│   ├── aktualnosci.html        ← strona publiczna: ogłoszenia + aktualności (dynamiczna)
│   ├── historia.html
│   ├── kontakt.html
│   ├── msze.html
│   ├── duszpasterstwo.html
│   ├── wspolnoty.html
│   ├── standardy.html
│   └── sakramenty/             ← podstrony sakramentów
├── admin/
│   ├── login.html              ← ekran logowania (brak auth — akceptuje cokolwiek)
│   ├── index.html              ← pulpit (dynamiczne statsy + aktywność + nadchodzące)
│   ├── aktualnosci.html        ← lista aktualności (tabela z filtrami)
│   ├── aktualnosci-edit.html   ← edytor wpisu (rich text, drag&drop zdjęć UI)
│   ├── ogloszenia.html         ← edytor ogłoszeń duszpasterskich
│   ├── galeria.html            ← galerie (siatka kart)
│   ├── intencje.html           ← kalendarz tygodniowy intencji mszalnych
│   ├── sakramenty.html         ← rejestr sakramentów (4 typy, pełny CRUD)
│   ├── pogrzeby.html           ← rejestr pogrzebów (pełny CRUD)
│   ├── parafianie.html         ← rejestr parafian (pełny CRUD)
│   ├── ustawienia.html         ← ustawienia parafii (dane, konta, godziny mszy)
│   └── assets/admin.css        ← współdzielony CSS całego panelu
├── public/img/                 ← zdjęcia parafii
├── build.py                    ← kopiuje zdjęcia z Kosciol/content/galeria/
├── README.md                   ← skrócona dokumentacja uruchomienia (dla klienta)
└── HANDOVER.md                 ← ten plik
```

---

## 3. localStorage — klucze i struktura danych

Wszystkie dane są współdzielone między panelem admina a stroną publiczną przez `localStorage`.

### Wzorzec (identyczny we wszystkich modułach)

```js
const LS_KEY     = 'nspj_XXX';    // klucz danych
const LS_VER_KEY = 'nspj_XXX_v';  // klucz wersji seeda
const DATA_VERSION = 1;           // liczba — jeśli stored < current → re-seed
```

### Klucze i ich właściciele

| Klucz localStorage | Właściciel (admin) | Czytane też przez |
|---|---|---|
| `nspj_aktualnosci` | `admin/aktualnosci.html` | `index.html`, `strony/aktualnosci.html` |
| `nspj_ogloszenia` | `admin/ogloszenia.html` | `index.html`, `strony/aktualnosci.html` |
| `nspj_intencje` | `admin/intencje.html` | `index.html`, `admin/index.html` |
| `nspj_sakramenty` | `admin/sakramenty.html` | `admin/index.html` |
| `nspj_pogrzeby` | `admin/pogrzeby.html` | `admin/index.html` |
| `nspj_parafianie` | `admin/parafianie.html` | `admin/index.html` |

### Schemat: `nspj_ogloszenia`
```js
{
  id: 'ogl-2026-05-24-1716550000000',
  title: 'VI Niedziela Wielkanocna',
  date: '2026-05-24',           // YYYY-MM-DD
  status: 'published' | 'draft',
  featured: true,               // tylko jedno = true → karta na index.html
  views: 320,
  content: '<p>...</p>'         // HTML z edytora rich text
}
```

### Schemat: `nspj_aktualnosci`
```js
{
  id: 'news-wizytacja',         // lub 'news-' + Date.now()
  title: 'Wizytacja kanoniczna abp. Galbasa',
  date: '2026-05-09',
  status: 'published' | 'draft',
  category: 'Wydarzenia',
  author: 'ks. Tomasz Żołna',
  excerpt: 'Krótki opis (do 200 znaków)',
  content: '<p>Pełna treść HTML</p>',
  image: '../public/img/event-wizytacja-1.jpg',
  tags: 'wizytacja, arcybiskup',
  featured: false,
  views: 920,
  slug: 'wizytacja-galbasa-2026',
  seoTitle: 'Wizytacja kanoniczna | Parafia NSPJ'
}
```

### Schemat: `nspj_intencje`
```js
{
  id: 'int-201',
  date: '2026-05-18',
  time: '18:00',
  intention: 'Za śp. Marię i Józefa Kowalskich w rocznicę śmierci',
  type: 'za_zm_pp' | 'za_zm_p' | 'w_int' | 'dziek'
}
```

### Schemat: `nspj_sakramenty`
```js
{
  bierzmowanie: [{ id, imie, nazwisko, data, imie_bierzmowania, kaplan, miejsce, rok }],
  chrzciny:     [{ id, imie, nazwisko, data_chrztu, kaplan, rodzice, ksiega_rok, ksiega_str, ksiega_nr }],
  sluby:        [{ id, oblubieniec, oblubienica, data_slubu, kaplan, miejsce }],
  komunia:      [{ id, imie, nazwisko, data, kaplan, rok }]
}
```

### Schemat: `nspj_pogrzeby`
```js
{
  id, imie, nazwisko, data_urodzenia, miejsce_urodzenia, rodzice,
  zamieszkanie, data_zgonu, data_pogrzebu, godzina, miejsce_ceremonii,
  kaplan, cmentarz, sektor, rzad, miejsce_grobu,
  status: 'Zgłoszony' | 'Zaplanowany' | 'Odbył się'
}
```

### Schemat: `nspj_parafianie`
```js
{
  id, imie, nazwisko, data_urodzenia, telefon, adres, email,
  sakr: { chrzest: bool, komunia: bool, bierzmowanie: bool, slub: bool },
  status: 'Aktywny' | 'Nieaktywny' | 'Kandydat',
  data_dolaczenia, uwagi
}
```

---

## 4. Stan modułów — co działa

| Moduł | Status | Uwagi |
|---|---|---|
| **Strona główna** `index.html` | ✅ | Dynamiczne: ogłoszenia, intencje, aktualności z localStorage |
| **Ogłoszenia** `admin/ogloszenia.html` | ✅ | Pełny CRUD, rich text, featured toggle, Ctrl+S |
| **Aktualności — lista** `admin/aktualnosci.html` | ✅ | Lista, filtry, tabela |
| **Aktualności — edytor** `admin/aktualnosci-edit.html` | ✅ | Rich text, SEO fields, zapis do localStorage |
| **Intencje mszalne** `admin/intencje.html` | ✅ | Kalendarz tygodniowy, CRUD, PDF trigger |
| **Sakramenty** `admin/sakramenty.html` | ✅ | 4 typy (bierzmowanie/chrzciny/śluby/komunia), 65 rekordów seed, pełna tabela ze wszystkimi polami, sticky scroll |
| **Pogrzeby** `admin/pogrzeby.html` | ✅ | 16 rekordów seed, 16 pól, sticky scroll, 4 kapłanów w select |
| **Parafianie** `admin/parafianie.html` | ✅ | 28 rekordów seed, sakramenty jako checkboxy, CSV export, paginacja |
| **Pulpit** `admin/index.html` | ✅ | Dynamiczne statsy + aktywność + nadchodzące wydarzenia z localStorage |
| **Galeria** `admin/galeria.html` | ⚠️ UI mock | Siatka kart, brak funkcjonalnego CRUD |
| **Ustawienia** `admin/ustawienia.html` | ⚠️ UI mock | Formularze, brak zapisu |
| **Strona publiczna: aktualności** `strony/aktualnosci.html` | ✅ | Ogłoszenia i aktualności z localStorage |

### Tabele z pełnymi polami (sticky scroll)

Wszystkie trzy rejestry (Sakramenty, Pogrzeby, Parafianie) mają:
- **`.tbl-wrap`** — `overflow-x: auto` wrapper
- **Sticky pierwsza kolumna** (imię/nazwisko) — `position: sticky; left: 0`
- **Sticky ostatnia kolumna** (Akcje) — `position: sticky; right: 0`
- **Poziomy scrollbar** — wszystkie pola z modalu edycji widoczne bez wchodzenia w edycję

---

## 5. CSS — ważne klasy (admin.css)

```
.tbl           — tabela (NIE .table-card — ta klasa nie istnieje)
.stat          — kafelek statystyki
.stats         — grid 4 kolumny
.stat .info .lbl / .num / .delta
.stat .ic      — ikona kafelka
.card / .card-head
.btn / .btn-primary / .btn-secondary / .btn-ghost / .btn-danger / .btn.sm
.pill-badge.pub / .draft / .arch
.form-row / .form-grid / .form-grid.cols-3
.tbl-wrap      — wrapper z overflow-x:auto + sticky kolumny (dodany w ostatniej sesji)
```

**Nigdy nie używaj:** `.table-card`, `.stat-card`, `.stat-val`, `.stat-label` — nie istnieją w admin.css.

---

## 6. Wzorzec działającego CRUD (do kopiowania)

`admin/ogloszenia.html` to wzorzec. Każdy moduł idzie tym schematem:

```
1. LS_KEY / LS_VER_KEY / DATA_VERSION — definicje kluczy
2. DEFAULT_XXX — tablica ~15 rekordów seed
3. loadData()   — JSON.parse(ls) || copy DEFAULT
4. saveData()   — JSON.stringify → localStorage
5. renderStats() — .stat .num + .delta
6. renderTable() — <div class="tbl-wrap"><table class="tbl">...
7. openModal(id) — wypełnia formularz
8. saveModal()  — zbiera z formularza → saveData → renderTable
9. del-banner pattern — potwierdzenie usunięcia
10. Toast — 2s komunikat
11. Init: if(storedVer < DATA_VERSION) re-seed; renderStats; renderTable
```

---

## 7. Co zostało zrobione w ostatniej sesji (maj 2026)

Zmiany od ostatniego HANDOVER.md (2026-05-27):

1. **`admin/pogrzeby.html`** — nowy plik, pełny CRUD, 16 pól, 16 rekordów seed
2. **`admin/parafianie.html`** — rewrite z UI mock na pełny CRUD, 28 rekordów seed, CSV export
3. **Tabele sticky** — `.tbl-wrap` + sticky first/last column dodany do Sakramentów, Pogrzebów i Parafian
4. **Pełne kolumny w tabelach** — wszystkie pola z modalu edycji widoczne w tabeli (scrollable)
5. **Sidebar ujednolicony** — link Pogrzeby dodany do wszystkich 9 plików admina; usunięto badge "Pkt 2" z Sakramenty i Parafianie
6. **Pulpit dynamiczny** — `admin/index.html`: statsy, feed aktywności i nadchodzące wydarzenia czytają z localStorage wszystkich modułów; data nagłówka dynamiczna
7. **Pobieranie TXT ogłoszeń** — `index.html`: przycisk "Pobierz TXT" generuje sformatowany plik z bieżącego ogłoszenia (Blob API)

---

## 8. Co należy zrobić w następnej kolejności

### 8A. Automatyczne SEO — PRIORYTET 1

Każda strona i każdy typ treści wymaga automatycznej generacji meta tagów z danych.

**Zakres:**

| Strona | Co generować automatycznie |
|---|---|
| `index.html` | `<title>`, `description` (statyczne, ale uzupełnić) |
| `strony/aktualnosci.html` | `<title>` = tytuł aktualności, `description` = excerpt, `og:image` = zdjęcie artykułu |
| Każdy artykuł aktualności | Canonical URL, `og:title`, `og:description`, `og:image`, `article:published_time`, `article:author` |
| Ogłoszenia | `<title>` = tytuł tygodnia, `description` = pierwsze zdanie treści |
| Strony statyczne (historia, kontakt, msze) | Uzupełnić puste `<meta name="description">` |

**Schemat implementacji (frontend, bez backendu):**

```html
<!-- W każdym pliku: placeholder tags do nadpisania przez JS -->
<title id="seo-title">Parafia NSPJ Czerwionka-Leszczyny</title>
<meta name="description" id="seo-desc" content="">
<meta property="og:title" id="og-title" content="">
<meta property="og:description" id="og-desc" content="">
<meta property="og:image" id="og-image" content="">
<link rel="canonical" id="seo-canonical" href="">
```

```js
// Na stronie aktualności — po załadowaniu artykułu z localStorage:
function applySEO(article) {
  var base = 'https://nspj-czerwionka.pl/';
  document.getElementById('seo-title').textContent = article.seoTitle || (article.title + ' | Parafia NSPJ');
  document.getElementById('seo-desc').content = article.excerpt || '';
  document.getElementById('og-title').content = article.title;
  document.getElementById('og-desc').content = article.excerpt || '';
  document.getElementById('og-image').content = article.image || base + 'public/img/og-default.jpg';
  document.getElementById('seo-canonical').href = base + 'strony/aktualnosci.html#' + article.id;
}
```

**Dla produkcji (backend):** SEO meta powinny być renderowane server-side (SSR w Astro) — boty Google nie wykonują JS. Demo może mieć JS-ową implementację jako proof-of-concept.

**Pole `seoTitle`** jest już w schemacie `nspj_aktualnosci` i w edytorze (`admin/aktualnosci-edit.html`). Wystarczy podpiąć.

**Sitemap XML** — do wygenerowania przy budowie backendu: `sitemap.xml` ze wszystkimi URL-ami artykułów, ogłoszeń i stron statycznych.

---

### 8B. Eksport do szablonu (template export) — PRIORYTET 2

Ogłoszenia duszpasterskie powinny dawać się eksportować do gotowego dokumentu (Word/PDF) do druku i rozesłania.

**Aktualny stan:** Przycisk "Generuj PDF" istnieje w `admin/ogloszenia.html` — wyzwala `window.print()` (print CSS).

**Do zaimplementowania:**

#### Opcja A — eksport DOCX (zalecana)
Użyć biblioteki `docx-js` (`npm install docx`) lub wbudować skrypt generujący `.docx` przez Blob:

```
Szablon dokumentu ogłoszeń:
┌──────────────────────────────────────┐
│ [Logo parafii]                       │
│ OGŁOSZENIA DUSZPASTERSKIE            │
│ [Tytuł niedzieli / święta]           │
│ [Data] · Parafia NSPJ Czerwionka     │
├──────────────────────────────────────┤
│ [Pełna treść ogłoszeń]               │
│                                      │
│ Ks. [imię proboszcza]                │
└──────────────────────────────────────┘
```

Wzorzec generowania DOCX przez przeglądarkę jest już w projekcie dla TXT:
- `index.html` — `downloadOgloszeniaTxt()` — Blob API, `URL.createObjectURL`
- Rozszerzyć o format DOCX używając `docx-js`

#### Opcja B — eksport PDF przez print CSS (tymczasowe)
`admin/ogloszenia.html` ma już `window.print()`. Wystarczy dodać `@media print` CSS z profesjonalnym layoutem (ukryć sidebar, menu, przyciski; wycentrować treść; dodać logo i stopkę). Działa bez backendu.

**Eksport CSV parafian** — już działa w `admin/parafianie.html` (BOM UTF-8, wszystkie pola).

---

## 9. Co zostało świadomie pominięte (poza zakresem demo)

| Funkcja | Powód pominięcia |
|---|---|
| **Moduł cmentarza** | Wykraczał poza zakres — osobny, rozbudowany temat |
| **Platforma online** (zapisy online, formularze, msze online) | Nie ten etap projektu |
| **Prawdziwy upload zdjęć** | Backend + storage — poza demo |
| **Autentykacja / logowanie** | Backend — akceptuje cokolwiek |
| **Wysyłka e-mail** | Backend |
| **Eksport PDF server-side** | Backend (Puppeteer/wkhtmltopdf) |
| **Galeria CRUD** | UI mock — priorytet niższy niż rejestry |
| **Ustawienia — zapis** | UI mock |

---

## 10. Stack docelowy (po akceptacji demo)

```
Frontend:   Astro (SSG/SSR) + islandki Alpine.js lub Vanilla JS
Backend:    Express.js (Node 20 LTS)
Baza:       SQLite (Turso lub lokalna na VPS)
Hosting:    Ubuntu 24 LTS + Nginx + PM2 + Let's Encrypt
CI/CD:      GitHub Actions → deploy na VPS przez SSH
```

---

## 11. Kontakty i dostępy

- **Repo:** `https://github.com/michalszafron-netizen/kosciolek`, branch `master`
- **Uruchomienie:** `python -m http.server 8765` → `http://localhost:8765`
- **Admin panel:** `http://localhost:8765/admin/index.html` (login: cokolwiek)
- **Projekt przygotowuje:** Michał Szafron (Netizen)
- **Klient:** Parafia NSPJ Czerwionka-Leszczyny, ks. Tomasz Żołna (proboszcz)

---

*HANDOVER zaktualizowany: 2026-05-28 | Sesja: pełny CRUD sakramenty/pogrzeby/parafianie + dynamiczny pulpit + sticky tabele*
