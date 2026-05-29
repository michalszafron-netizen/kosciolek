# Automatyczne SEO — Parafia NSPJ Czerwionka-Leszczyny

> **Plik:** `docs/SEO-automatyczne.md`  
> **Dotyczy:** `demo-parafia-v2/`  
> **Ostatnia aktualizacja:** maj 2026

---

## 1. Co to jest i po co to działa?

Strona parafii używa **dynamicznego systemu SEO**, który automatycznie aktualizuje metadane strony (`<title>`, `<meta description>`, Open Graph, Twitter Card, canonical URL) w zależności od tego, co aktualnie wyświetla się użytkownikowi.

Dzięki temu:
- każdy artykuł z aktualności i każde ogłoszenie ma **unikalny, opisowy tytuł i opis** w wynikach wyszukiwarki Google,
- linki udostępniane na Facebooku/Instagramie pokazują **właściwy tytuł, opis i miniaturę** (nie ogólne dane parafii),
- adres URL jest prawidłowy dla każdego widoku (canonical), co zapobiega duplikowaniu treści w oczach Google.

---

## 2. Zakres działania

System automatycznego SEO działa **wyłącznie** na stronie:

```
strony/aktualnosci.html
```

Wszystkie pozostałe strony (`msze.html`, `kontakt.html`, sakramenty itd.) mają **statyczne** metadane — stałe, wpisane bezpośrednio w HTML. One nigdy się nie zmieniają automatycznie, bo ich treść jest zawsze taka sama.

---

## 3. Trzy tryby widoku i jak zmienia się SEO

Strona `aktualnosci.html` ma trzy stany. System SEO reaguje na każdy z nich:

### Tryb A — Lista (domyślny widok po wejściu)
Widoczna jest lista kart aktualności lub zakładka ogłoszeń bez wybranego ogłoszenia.

```
URL:     strony/aktualnosci.html  lub  #aktualnosci
Title:   Ogłoszenia i aktualności · Parafia NSPJ Czerwionka-Leszczyny
Desc:    Cotygodniowe ogłoszenia duszpasterskie, aktualności z życia parafii...
Obraz:   zdjęcie kościoła (domyślne)
```

---

### Tryb B — Artykuł aktualności (hash `#news-`)
Użytkownik kliknął kartę aktualności lub wszedł bezpośrednio przez link z hashem, np.:

```
strony/aktualnosci.html#news-wizytacja
```

SEO automatycznie aktualizuje się do:

```
Title:   [seoTitle lub title artykułu] · Parafia NSPJ Czerwionka-Leszczyny
Desc:    [excerpt artykułu, max 200 znaków]
Obraz:   [miniatura artykułu, jeśli ustawiona; inaczej domyślna]
URL:     https://www.nspjczerwionka.pl/strony/aktualnosci.html#news-wizytacja
```

Dane są pobierane z obiektu artykułu zapisanego w `localStorage` pod kluczem `nspj_aktualnosci`.

---

### Tryb C — Ogłoszenie (hash `#ogl-`)
Użytkownik przełączył się na zakładkę Ogłoszenia i wybrał konkretny tydzień, np.:

```
strony/aktualnosci.html#ogl-2026-05-25
```

SEO automatycznie aktualizuje się do:

```
Title:   Ogłoszenia: [tytuł ogłoszenia] · Parafia NSPJ Czerwionka-Leszczyny
Desc:    [pierwsze 200 znaków treści ogłoszenia, bez tagów HTML]
URL:     https://www.nspjczerwionka.pl/strony/aktualnosci.html#ogl-2026-05-25
```

Dane są pobierane z obiektu ogłoszenia zapisanego w `localStorage` pod kluczem `nspj_ogloszenia`.

---

## 4. Jak to działa technicznie?

### 4.1 Dwie funkcje JS odpowiedzialne za SEO

W pliku `strony/aktualnosci.html`, w bloku `<script>` przy końcu strony, znajdują się dwie kluczowe funkcje:

#### `updateSEOMeta(type, data)`

Przyjmuje typ widoku (`'article'`, `'announcement'` lub domyślnie `'list'`) i obiekt danych, a następnie aktualizuje wszystkie tagi w `<head>`:

| Tag HTML | Co aktualizuje |
|---|---|
| `document.title` | Tytuł zakładki przeglądarki |
| `<meta name="description">` | Opis strony |
| `<meta property="og:title">` | Tytuł dla Facebooka/Instagrama |
| `<meta property="og:description">` | Opis dla Facebooka/Instagrama |
| `<meta property="og:image">` | Miniatura dla Facebooka/Instagrama |
| `<meta property="og:url">` | Aktualny URL widoku |
| `<meta name="twitter:*">` | Analogicznie dla Twittera/X |
| `<link rel="canonical">` | Kanoniczny URL dla Google |

#### `syncSEOFromView()`

Odczytuje aktualny hash z `location.hash` i na tej podstawie decyduje, który tryb SEO uruchomić:

```
hash zaczyna się od "news-"  →  tryb B (artykuł)
hash zaczyna się od "ogl-"   →  tryb C (ogłoszenie)
brak hasha / inny hash       →  tryb A (lista)
```

### 4.2 Kiedy `syncSEOFromView()` jest wywoływane?

Funkcja jest podłączona do wszystkich zdarzeń, które zmieniają widok:

| Zdarzenie | Plik / miejsce |
|---|---|
| Kliknięcie karty artykułu (przejście do pełnego widoku) | `showArticle(id)` |
| Kliknięcie przycisku „powrót do listy" | `back-to-list` click handler |
| Kliknięcie zakładki (Aktualności / Ogłoszenia) | `.page-tab-btn` click handler |
| Kliknięcie innego ogłoszenia w navie bocznym | `showOgl(id)` |
| Wejście bezpośrednie przez URL z hashem | IIFE inicjalizująca stronę (na dole `<script>`) |

---

## 5. Skąd system bierze dane?

System korzysta z tych samych danych co reszta strony — `localStorage` przeglądarki.

### Aktualności
```js
// Klucz: nspj_aktualnosci
// Pola używane przez SEO:
{
  id:       "news-wizytacja",   // identyfikator (hash w URL)
  title:    "Wizytacja biskupia",
  seoTitle: "Wizytacja Biskupa — relacja z uroczystości",  // opcjonalne, priorytetowe
  excerpt:  "W niedzielę 25 maja nasza parafia gościła...",
  image:    "public/img/wizytacja.jpg"  // opcjonalne
}
```

> **Ważne:** Jeśli artykuł ma wypełnione pole `seoTitle` (ustawiane w panelu admina → edytor aktualności), to właśnie ono pojawi się jako tytuł strony i tytuł karty OG. Jeśli puste — użyty zostanie zwykły `title`.

### Ogłoszenia
```js
// Klucz: nspj_ogloszenia
// Pola używane przez SEO:
{
  id:      "ogl-2026-05-25",
  title:   "Ogłoszenia parafialne — 25 maja 2026",
  content: "<p>...</p>"  // HTML, z którego wyciągany jest tekst jako description
}
```

---

## 6. Jak SEO działa przy publikacji artykułu? (Krok po kroku)

Przykład: administrator publikuje artykuł o wizytacji biskupa.

```
1. Admin wchodzi do:  admin/aktualnosci-edit.html
2. Wypełnia pola:
   - Tytuł:         "Wizytacja biskupia"
   - SEO Title:     "Wizytacja Biskupa — relacja z uroczystości"  ← opcjonalne!
   - Fragment:      "W niedzielę nasza parafia gościła..."
   - Zdjęcie:       wybiera zdjęcie
3. Klika „Opublikuj" → artykuł zapisywany do localStorage (klucz: nspj_aktualnosci)

4. Użytkownik wchodzi na: strony/aktualnosci.html
   → SEO: tryb A (lista) — ogólny tytuł parafii

5. Użytkownik klika kartę artykułu
   → showArticle("news-wizytacja") wywołuje syncSEOFromView()
   → SEO: tryb B — tytuł = "Wizytacja Biskupa — relacja z uroczystości · Parafia NSPJ..."
              desc  = "W niedzielę nasza parafia gościła..."
              obraz = zdjęcie z artykułu

6. Użytkownik kopiuje URL i wkleja na Facebook
   → Facebook odczytuje og:title i og:image z <head>
   → Karta pokazuje właściwy tytuł i miniaturę artykułu ✓

7. Użytkownik klika „Powrót do listy"
   → syncSEOFromView() → tryb A → ogólny tytuł parafii wraca ✓
```

---

## 7. Ograniczenia i uwagi

### ⚠️ Hash w URL a Google

Google **indeksuje URL-e z hashem** (`#news-xyz`), ale jest to mechanizm po stronie klienta (JavaScript). Oznacza to, że:

- Google może nie zawsze zaindeksować pełny artykuł jako osobny wynik
- Bardziej niezawodne byłoby SSR lub generowanie statycznych podstron dla każdego artykułu

Dla demo HTML/JS bez backendu — obecne rozwiązanie jest **optymalne** i spełnia wszystkie możliwości client-side SEO.

### ⚠️ Open Graph i Facebook

Facebook buforuje metadane OG. Przy udostępnianiu linku z hashem (`#news-xyz`) Facebook może nie odczytać zaktualizowanych tagów OG (bot Facebooka nie wykonuje JS). Rozwiązanie docelowe (backend) powinno generować osobne strony dla każdego artykułu ze statycznym `<head>`.

### ✅ Co działa w pełni

- Aktualizacja tytułu zakładki przeglądarki przy każdej zmianie widoku
- Prawidłowy `canonical` URL dla Google
- Właściwe tagi meta description dla każdego widoku
- Spójny `og:image` i `og:title` przy kopiowaniu linku

---

## 8. Pliki objęte systemem SEO

| Plik | Typ SEO | Opis |
|---|---|---|
| `index.html` | Statyczne | JSON-LD `Church` + OG + canonical |
| `strony/aktualnosci.html` | **Dynamiczne** | JS aktualizuje przy każdej zmianie widoku |
| `strony/duszpasterstwo.html` | Statyczne | Canonical + OG + Breadcrumbs JSON-LD |
| `strony/historia.html` | Statyczne | Canonical + OG + Breadcrumbs JSON-LD |
| `strony/kontakt.html` | Statyczne | Canonical + OG + Breadcrumbs JSON-LD |
| `strony/msze.html` | Statyczne | Canonical + OG + Breadcrumbs JSON-LD |
| `strony/standardy.html` | Statyczne | Canonical + OG + Breadcrumbs JSON-LD |
| `strony/wspolnoty.html` | Statyczne | Canonical + OG + Breadcrumbs JSON-LD |
| `strony/sakramenty/*.html` | Statyczne | Canonical + OG + Breadcrumbs JSON-LD (3 poziomy) |
| `sitemap.xml` | Statyczny plik | 15 URL-i z priorytetami dla robotów Google |

---

## 9. Sitemap

Plik `sitemap.xml` w katalogu głównym `demo-parafia-v2/` zawiera listę wszystkich 15 publicznych podstron serwisu z priorytetami:

| Priorytet | Strony |
|---|---|
| `1.0` | Strona główna |
| `0.9` | Aktualności, Msze święte |
| `0.8` | Kontakt |
| `0.7` | Duszpasterstwo, Wspólnoty |
| `0.6` | Historia, Sakramenty (Chrzest, Komunia, Bierzmowanie, Ślub, Spowiedź) |
| `0.5` | Standardy ochrony, Namaszczenie, Pogrzeb |

Plik należy przesłać do Google Search Console po wdrożeniu produkcyjnym.

---

*Dokumentacja wygenerowana w ramach zadania 8A — Automatyczne SEO, maj 2026.*
