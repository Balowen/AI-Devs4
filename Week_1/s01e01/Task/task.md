## Jak działają zadania w kursie

W trakcie kursu, pod lekcją w każdym dniu będzie pojawiać się jedno zadanie. Większość z nich wymaga wykonania kilku kroków i zgłoszenia poprawnej odpowiedzi do Centrali, czyli naszego hubu.

Hub ma swoją stronę internetową pod adresem: [https://hub.ag3nts.org/](https://hub.ag3nts.org/). Logowanie do hubu jest przez EasyCart, czyli system, w którym kupowaliście kurs. Na stronie hubu, w jego górnej części znajdziesz swój klucz API (więcej o nim poniżej). Jest tam też licznik punktów z zadań i punktów z zadań sekretnych. Poniżej znajduje się pole do wpisania zdobytych flag za zadania i sekrety. Plansza w głównej części strony pokazuje Twoje postępy. Pamiętaj, że do zdobycia certyfikatu wystarczy zdobycie 20 punktów z zadań podstawowych (sekrety nie liczą się do certyfikatu).

Jeśli chodzi o zdobywanie flag podczas rozwiązywania zadań, to zazwyczaj otrzymujesz je po wysłaniu poprawnej odpowiedzi do API hubu. Zgłoszenie odpowiedzi to wywołanie requestu POST z body w formacie JSON:

```json
{
  "apikey": "tutaj-twój-klucz-api",
  "task": "nazwa-zadania",
  "answer": "tutaj-odpowiedz-w-formie-wymaganej-przez-zadanie"
}
```

Hub odpowiada komunikatami o błędach lub informacją o zdobytej fladze. Flaga ma format `{FLG:....}`. Zdobytą w ten sposób flagę wpisujesz na stronie hubu i zdobywasz punkt. Flagę można wpisać zarówno w całości, jak i samą część po `FLG:`, czyli w przypadku kiedy otrzymasz `{FLG:PIZZA}`, w hubie możesz podać zarówno `{FLG:PIZZA}`, jak i `PIZZA`.

## Zadanie

Pobierz listę osób, które przeżyły 'Wielką Korektę' i które współpracują z systemem. Znajdziesz ją pod linkiem:
[https://hub.ag3nts.org/data/tutaj-twój-klucz/people.csv](https://hub.ag3nts.org/data/tutaj-tw%C3%B3j-klucz/people.csv)

Wiemy, że do organizacji transportów między elektrowniami angażowani są ludzie, którzy:

- są mężczyznami, którzy teraz w 2026 roku mają między 20, a 40 lat
- urodzonych w Grudziądzu
- pracują w branży transportowej

Każdą z potencjalnych osób musisz odpowiednio otagować. Mamy do dyspozycji następujące tagi:

- IT
- transport
- edukacja
- medycyna
- praca z ludźmi
- praca z pojazdami
- praca fizyczna

Jedna osoba może mieć wiele tagów. Nas interesują tylko ludzie pracujący w transporcie, którzy spełniają też poprzednie warunki.

Prześlij nam listę osób, którymi powinniśmy się zainteresować. Oczekujemy formatu odpowiedzi jak poniżej, wysłanego na adres https://hub.ag3nts.org/verify

Nazwa zadania to: **people**.

```json
{
       "apikey": "tutaj-twój-klucz-api",
       "task": "people",
       "answer": [
         {
           "name": "Jan",
           "surname": "Kowalski",
           "gender": "M",
           "born": 1987,
           "city": "Warszawa",
           "tags": ["tag1", "tag2"]
         },
         {
           "name": "Anna",
           "surname": "Nowak",
           "gender": "F",
           "born": 1993,
           "city": "Grudziądz",
           "tags": ["tagA", "tagB", "tagC"]
         }
       ]
     }
```

### Co należy zrobić w zadaniu?

1. **Pobierz dane z hubu** - plik `people.csv` dostępny pod linkiem z treści zadania (wstaw swój klucz API z https://hub.ag3nts.org/). Plik zawiera dane osobowe wraz z opisem stanowiska pracy (`job`).
2. **Przefiltruj dane** - zostaw wyłącznie osoby spełniające wszystkie kryteria: płeć, miejsce urodzenia, wiek.
3. **Otaguj zawody modelem językowym** - wyślij opisy stanowisk (`job`) do LLM i poproś o przypisanie tagów z listy dostępnej w zadaniu. Użyj mechanizmu Structured Output, aby wymusić odpowiedź modelu w określonym formacie JSON. Szczegóły we Wskazówkach.
4. **Wybierz odpowiednie osoby** - z otagowanych rekordów wybierz wyłącznie te z tagiem `transport`.
5. **Wyślij odpowiedź** - prześlij tablicę obiektów na adres `https://hub.ag3nts.org/verify` w formacie pokazanym powyżej (nazwa zadania: `people`).
6. **Zdobycie flagi** - jeśli wysłane dane będą poprawne, Hub w odpowiedzi odeśle flagę w formacie {FLG:JAKIES_SLOWO} - flagę należy wpisać pod adresem: https://hub.ag3nts.org/ (wejdź na tą stronę w swojej przeglądarce, zaloguj się kontem którym robiłeś zakup kursu i wpisz flagę w odpowiednie pole na stronie)

### Wskazówki

- **Structured Output - cel i sposób użycia:** Celem zadania jest zastosowanie mechanizmu Structured Output przy klasyfikacji zawodów przez LLM. Polega on na wymuszeniu odpowiedzi modelu w ściśle określonym formacie JSON przez przekazanie schematu (JSON Schema) w polu `response_format` wywołania API. Dokumentacja: [OpenAI](https://platform.openai.com/docs/guides/structured-outputs#supported-schemas), [Anthropic](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [Gemini](https://ai.google.dev/gemini-api/docs/structured-output?example=recipe). Zadanie da się rozwiązać bez Structured Output, na przykład prosząc model o zwrócenie JSON-a i parsując go ręcznie - ale Structured Output eliminuje całą klasę błędów. Możesz też użyć bibliotek jak **Instructor** ([Python](https://python.useinstructor.com/)/[JS/TypeScript](https://js.useinstructor.com/)), które obsługują ten mechanizm za Ciebie.
- **Batch tagging - jedno wywołanie dla wielu rekordów:** Zamiast wywoływać LLM osobno dla każdej osoby, możesz na przykład wysłać w jednym żądaniu ponumerowaną listę opisów stanowisk i poprosić o zwrócenie listy obiektów z numerem rekordu i przypisanymi tagami. Znacznie zredukuje to liczbę wywołań API.
- **Opisy tagów pomagają modelowi:** Do każdej kategorii dołącz krótki opis zakresu - pomaga to modelowi poprawnie sklasyfikować niejednoznaczne stanowiska.
- **Format pól w odpowiedzi:** Pole `born` to liczba całkowita (sam rok urodzenia). Pole `tags` to tablica stringów, nie jeden string z przecinkami.

## Linki do filmu Mateusza

1. Przed wyruszeniem w drogę trzeba zebrać drużynę modeli [https://youtu.be/X2kWqlSnX1E?list=PL6gb3F2o2zOTJYxrcnWphmGLylXIlVCGJ](https://youtu.be/X2kWqlSnX1E?list=PL6gb3F2o2zOTJYxrcnWphmGLylXIlVCGJ), [https://arxiv.org/abs/2601.05106](https://arxiv.org/abs/2601.05106)
2. Współpraca między modelami [https://www.youtube.com/watch?v=DJI2XC71BlA&list=PL6gb3F2o2zOTJYxrcnWphmGLylXIlVCGJ&index=6](https://www.youtube.com/watch?v=DJI2XC71BlA&list=PL6gb3F2o2zOTJYxrcnWphmGLylXIlVCGJ&index=6), [https://arxiv.org/abs/2601.05167](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbVdUZWVFdU05aEU3aDhUX0RCUWtsUGhlT2xZUXxBQ3Jtc0trdmIzNGFPY1RnUjJOaUUyczNYOGtOODltNDNXNExqMlBfQzBmRlFlVXllbTd3VlpVWXVTTlJxdUg4UmtqcW1rQUxfQXBEczdxd3JRWkJoSDVjaE1Mdjk4R2Y0ZG5sUlpnRDhuSHp5Wlg2T0tiSUVENA&q=https%3A%2F%2Farxiv.org%2Fabs%2F2601.05167&v=DJI2XC71BlA)
