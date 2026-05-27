# Handover: Demo Parafia NSPJ — stan projektu i znane bugi

> Dokument dla developera przejmującego sesję.  
> Data: 2026-05-27  
> Projekt: `demo-parafia-v2` (UI/UX demo, brak backendu)

---

## 1. Co to jest

**Statyczne demo HTML/CSS/JS** landing page + panel admina dla parafii NSPJ Czerwionka-Leszczyny.  
Brak backendu — cały stan aplikacji przechowywany w **`localStorage` przeglądarki**.  
Po akceptacji UI powstanie backend: Astro + Express + SQLite na VPS.

Uruchomienie:
```bash
cd demo-parafia-v2
python -m http.server 8765
# → http://localhost:8765
```

---

## 2. Struktura plików

```
demo-parafia-v2/
├── index.html                  ← strona główna
├── strony/
│   ├── aktualnosci.html        ← strona publiczna: ogłoszenia + aktualności
│   ├── historia.html
│   └── kontakt.html
├── admin/
│   ├── login.html
│   ├── index.html              ← pulpit admina
│   ├── aktualnosci.html        ← lista aktualności (tabela)
│   ├── aktualnosci-edit.html   ← edytor wpisu aktualności
│   ├── ogloszenia.html         ← edytor ogłoszeń duszpasterskich
│   ├── galeria.html
│   ├── intencje.html
│   ├── ustawienia.html
│   └── assets/admin.css
└── public/img/                 ← zdjęcia parafii
```

---

## 3. Architektura danych (localStorage)

Dwa niezależne klucze w localStorage, współdzielone między admin a stroną publiczną:

### `nspj_ogloszenia` — ogłoszenia duszpasterskie
```js
[
  {
    id: 'ogl-2026-05-24-1716550000000',  // 'ogl-' + data + '-' + timestamp
    title: 'VI Niedziela Wielkanocna',
    date: '2026-05-24',
    status: 'published' | 'draft',
    featured: true,          // tylko jedno może być true — wyświetlane na index.html
    views: 320,
    content: '<p>...</p>'    // HTML z rich-text edytora
  }
]
```

**Działa w 100%:**
- `admin/ogloszenia.html` — pełny edytor, lista archiwum, dodawanie, usuwanie, toggle featured
- `strony/aktualnosci.html` (tab "Ogłoszenia duszpasterskie") — czyta localStorage, renderuje sidebar + pełne panele
- `index.html` — karta "Ogłoszenia parafialne" aktualizuje się dynamicznie (pokazuje `featured: true` lub najnowsze)

---

### `nspj_aktualnosci` — aktualności parafialne
```js
[
  {
    id: 'news-wizytacja',            // lub 'news-' + Date.now() dla nowych
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
]
```

**Ten klucz ma bugi — patrz sekcja 5.**

---

## 4. Co działa poprawnie

| Funkcja | Plik | Status |
|---|---|---|
| Ogłoszenia — edytor (B/I/U/H2/H3/listy) | `admin/ogloszenia.html` | ✅ |
| Ogłoszenia — dodawanie nowego (modal, auto-data niedzieli) | `admin/ogloszenia.html` | ✅ |
| Ogłoszenia — usuwanie z potwierdzeniem | `admin/ogloszenia.html` | ✅ |
| Ogłoszenia — "Pokaż na stronie głównej" (featured) | `admin/ogloszenia.html` | ✅ |
| Ogłoszenia — zapis do localStorage, toast, Ctrl+S | `admin/ogloszenia.html` | ✅ |
| Ogłoszenia publiczne — dynamiczny rendering z localStorage | `strony/aktualnosci.html` | ✅ |
| Ogłoszenia — sidebar + panele nawigacja hash | `strony/aktualnosci.html` | ✅ |
| Karta ogłoszeń na homepage — dynamiczna (featured/latest) | `index.html` | ✅ |
| Aktualności — lista w adminie (tabela HTML) | `admin/aktualnosci.html` | ❌ BUG |
| Aktualności — edytor wpisu | `admin/aktualnosci-edit.html` | ❌ BUG |
| Aktualności — strona publiczna (karty + artykuł) | `strony/aktualnosci.html` | ❌ CZĘŚCIOWO |
| Aktualności — 2 karty na homepage | `index.html` | ❌ BUG |
| Nawigacja admin ↔ public (linki, login) | wszystkie | ✅ |
| Responsywność, hero slider, intencje, galeria (UI mock) | `index.html`, `admin/` | ✅ |

---

## 5. ZNANE BUGI — aktualności

### Bug A — `admin/aktualnosci.html` pokazuje pustą tabelę

**Objaw:** Strona ładuje się, ale `<tbody id="news-tbody">` jest pusty — zero wierszy.

**Gdzie:** `admin/aktualnosci.html`, cały `<script>` na dole pliku (wstawiony przez Python po `</body>`).

**Podejrzana przyczyna:**  
JS blok zawiera ciągi znaków z polskimi literami (tytuły artykułów w `DEFAULT_NEWS`) zakodowane jako ASCII przez skrypt Pythona (np. `'Wizytacja kanoniczna abp. Galbasa'` — bez polskich znaków). To samo w sobie nie powoduje błędu JS, ale **gdzieś w tym bloku może być syntax error** który urywa wykonanie zanim dotrze do `renderTable()`.

**Jak zdiagnozować:**
1. Otwórz `http://localhost:8765/admin/aktualnosci.html`
2. DevTools → Console (F12) → szukaj **czerwonych błędów**
3. DevTools → Console → wpisz: `localStorage.getItem('nspj_aktualnosci')` — czy cokolwiek jest?
4. DevTools → Console → wpisz: `renderTable()` ręcznie — czy tabela się wypełni?

**Żeby naprawić:**  
Najprościej **zastąpić cały `<script>` blok** na końcu `admin/aktualnosci.html` świeżo napisanym JS (nie generowanym przez Python). Logika jest prosta:

```js
const LS_KEY = 'nspj_aktualnosci';

// DEFAULT_NEWS — 8 artykułów (patrz niżej)
// loadNews() — czyta localStorage, fallback do DEFAULT_NEWS
// saveNews() — zapisuje do localStorage
// renderTable() — iteruje allNews, buduje <tr> dla każdego artykułu
// Filtry: .tab[data-filter] click → zmienia currentFilter → renderTable()
// Delete: data-delete button → del-banner → saveNews → renderTable
// Search: input event → ukrywa/pokazuje wiersze
// Init: if(!localStorage.getItem(LS_KEY)) saveNews(allNews); renderTable();
```

Wzorzec do skopiowania: `admin/ogloszenia.html` — ten plik działa identycznie i ma tę samą architekturę.

---

### Bug B — `admin/aktualnosci-edit.html` — puste pola / "Artykuł nie istnieje"

**Objaw:** Po kliknięciu „Edytuj" przy dowolnym artykule w liście, edytor otwiera się z pustymi polami lub komunikatem "Wczytywanie…".

**Przyczyna:**  
Edytor ładuje dane tak:
```js
const params = new URLSearchParams(location.search);
const editId = params.get('id');   // np. 'news-100lat'
let allNews = loadAllNews();       // czyta localStorage
let currentArticle = allNews.find(a => a.id === editId);
```

Jeśli localStorage jest pusty (Bug A sprawia że lista nigdy nie zapisała defaults), `loadAllNews()` wraca do `DEFAULT_NEWS` w edytorze. `DEFAULT_NEWS` edytora ma teraz 8 artykułów (zostały naprawione). Ale jeśli localStorage zawiera stare/złe dane z poprzedniej sesji — artykuł może nie zostać znaleziony.

**Jak zdiagnozować:**
1. DevTools → Console → `localStorage.getItem('nspj_aktualnosci')` — co zwraca?
2. Jeśli `null` → Bug A nie zapisał defaults → edytor powinien używać swoich DEFAULT_NEWS
3. Jeśli zwraca stare dane z inną strukturą → `JSON.parse()` i sprawdź czy `id` pasują

**Żeby naprawić:**  
```js
// Na początku skryptu edytora, po loadAllNews():
let allNews = loadAllNews();
if (!localStorage.getItem(LS_KEY)) {
  saveAllNews(allNews); // seed defaults do localStorage
}
// Ta linia już jest w pliku — sprawdź czy działa
```

Dodatkowo: upewnij się że `populateForm(currentArticle)` jest wywoływane TYLKO gdy `currentArticle !== null`.

---

### Bug C — `index.html` — karty aktualności nie aktualizują się

**Objaw:** Na homepage zawsze widać zakodowane na stałe artykuły „Wizytacja" i „Budowa wieży", nawet po dodaniu nowych aktualności w adminie.

**Gdzie:** `index.html`, linia ~977, `<script>` tuż przed `<!-- OGŁOSZENIA DYNAMICZNE -->`.

**Przyczyna:**  
Skrypt jest poprawny logicznie:
```js
(function() {
  var raw = localStorage.getItem('nspj_aktualnosci');
  var data = raw ? JSON.parse(raw) : null;
  // ...
  if (!published || published.length === 0) return; // ← jeśli localStorage pusty → return
  // ...
  fillCard(1, published[0]);
  fillCard(2, published[1]);
})();
```

Skrypt zwraca `return` gdy localStorage jest pusty — co przy Bug A (localStorage nie jest seedowany) oznacza że **fallback hardkodowany nigdy nie zostaje nadpisany**.

**Rozwiązanie:**  
Bug C rozwiąże się sam gdy Bug A zostanie naprawiony i `nspj_aktualnosci` znajdzie się w localStorage. Można też dodać fallback bezpośrednio w `index.html` używając `DEFAULT_NEWS` — ale lepiej najpierw naprawić Bug A.

---

## 6. Pliki do przejrzenia (ważność malejąca)

| Plik | Rola | Uwagi |
|---|---|---|
| `admin/aktualnosci.html` | Lista aktualności w adminie | **Cały `<script>` wymaga rewrite** |
| `admin/aktualnosci-edit.html` | Edytor wpisu | JS działa, ale zależy od localStorage |
| `strony/aktualnosci.html` | Strona publiczna | Ogłoszenia ✅, aktualności 90% (bug fix zrobiony dziś) |
| `index.html` | Strona główna | Ogłoszenia ✅, aktualności czekają na Bug A |
| `admin/ogloszenia.html` | Edytor ogłoszeń | **W pełni działa — wzorzec do naśladowania** |

---

## 7. Wzorzec działającego kodu (do skopiowania)

`admin/ogloszenia.html` to jedyna w pełni działająca implementacja. Wzorzec:

```
1. DEFAULT_DATA — tablica domyślnych obiektów (fallback)
2. loadData()   — JSON.parse(localStorage.getItem(KEY)) || DEFAULT_DATA copy
3. saveData()   — localStorage.setItem(KEY, JSON.stringify(data))
4. renderList() — czyści kontener, buduje innerHTML z tablicy
5. loadItem(id) — wypełnia formularz danymi wybranego elementu
6. saveItem()   — zbiera z formularza, updateuje tablicę, saveData(), renderList()
7. Init:
     let data = loadData();
     if (!localStorage.getItem(KEY)) saveData(data);  // seed
     renderList();
     if (data[0]) loadItem(data[0].id);               // załaduj pierwszy
```

---

## 8. Szybki test po naprawie

```
1. Otwórz http://localhost:8765/admin/aktualnosci.html
   → powinna być tabela z 8 wierszami
   
2. Kliknij "Edytuj" przy "Wizytacja kanoniczna"
   → edytor powinien załadować tytuł, treść, datę, kategorię itd.
   
3. Zmień tytuł → "Opublikuj"
   → toast "Aktualność opublikowana"
   
4. Wróć do listy → zmieniony tytuł widoczny w tabeli
   
5. Otwórz http://localhost:8765/strony/aktualnosci.html → tab "Aktualności parafialne"
   → zmieniony tytuł widoczny w karcie
   
6. Kliknij "Czytaj dalej →"
   → artykuł otwiera się z pełną treścią
   
7. Otwórz http://localhost:8765/index.html
   → sekcja "Ogłoszenia i aktualności" — 2 karty z najnowszymi artykułami
```

---

## 9. Co NIE jest zaimplementowane (celowo — to UI demo)

- Backend (żaden endpoint nie istnieje)
- Prawdziwy upload zdjęć (pole URL działa, drag&drop jest dekoracyjny)
- Wysyłka e-mail (checkbox istnieje, ale nic nie wysyła)
- PDF export (przycisk wyzwala `window.print()`)
- Autentykacja (login akceptuje cokolwiek)
- Paginacja w adminie (UI jest, JS jej nie obsługuje)

---

*Dokument wygenerowany: 2026-05-27*
