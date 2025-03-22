# Projekt 1 - Problem jedzących filozofów (ang. _Dining philosophers problem_)

Aplikacja napisana w języku C++, wykorzystująca wielowątkowość oraz mechanizmy zabezpieczające sekcje krytyczne: mutexy i semafory, rozwiązująca problem jedzących filozofów metodą Dijkstry.


## Wymagania systemowe
* Kompilator języka C++ kompatybilny z C++ 20 (np. _g++ 10+_, _clang 11+_)
* Emulator terminalu lub wiersz polecenia
* Zainstalowany _make_ (opcjonalnie)


## Instrukcja uruchomienia projektu

1. **Pobierz projekt**

      ```bash
      git clone https://github.com/szymic7/SO2_projekt.git
      cd SO2_projekt
      ```

2. **Zmień katalog na folder z projektem 1**

      ```bash
      cd projekt1
      ```

3. **Skompiluj program**

* Z użyciem Makefile

    ```bash
    make
    ```

* Bez użycia Makefile

  * Windows:

      ```bash
      g++ -std=c++20 -o SO2_projekt1.exe main.cpp DiningPhilosophers.cpp
      ```
  
  * Linux/MacOS:

      ```bash
      g++ -std=c++20 -pthread -o SO2_projekt1 main.cpp DiningPhilosophers.cpp
      ```

4. **Uruchom skompilowany program, podając jako argument liczbę filozofów (wątków)**

* Windows:

    ```bash
    SO2_projekt1.exe 5
    ```

* Linux/MacOS:

    ```bash
    ./SO2_projekt1 5
    ```


## Opis problemu

**Problem jedzących (ucztujących) filozofów** (ang. _**Dining philosophers problem**_) jest prostym przykładem zadania synchronizacji procesów. Podwaliny problemu stanowi zaproponowane w 1965 r. przez Edsgera Dijkstrę zadanie egzaminacyjne, w którym to 5 komputerów próbowało uzyskać dostęp do 5 współdzielonych napędów dysków. Problem jedzących filozofów sformułowałowany został niewiele później przez Charlesa Hoare’a. 

Problem przedstawia się następująco: pewna liczba filozofów (w oryginalnej wersji problemu było ich pięciu) siedzi przy stole. Każdy z nich wykonuje w danym momencie jedną z dwóch czynności - rozmyśla lub je. Każdy z filozofów ma przed sobą miskę z jedzeniem (spaghetti), a z jej obu stron po jednym widelcu. Zakłada się, że do jedzenia filozof potrzebuje dwóch widelców, przy czym dany myśliciel może podnieść jedynie sztućce leżące bezpośrednio przed nim. Problem stwarza niebezpieczeństwo zakleszczenia, w sytuacji, gdy każdy z filozofów podniesie widelec leżący po swojej prawej stronie (lub lewej). W takim wypadku, bez odpowiedniego podejścia do problemu, filozofowie będą czekać w nieskończoność, aż ich sąsiad zwolni widelec (współdzielony zasób). 

Istnieje kilka metod, za pomocą których można rozwiązać problem ucztujących filozofów. Do najczęściej stosowanych należy wykorzystanie kelnera (nazywanego też arbitrem), hierarchizacja zasobów oraz metoda Dijkstry, która została zaimplementowana w utworzonej aplikacji.


## Rozwiązanie Dijkstry

Dijkstra, konstruując rozwiązanie problemu, założył, że dany filozof chcąc jeść, albo podnosi oba widelce, albo nie podnosi żadnego w nich, eliminując w ten sposób sytuację, w której dany myśliciel trzyma jeden widelec, czekając aż jego sąsiad zwolni drugi z potrzebnych sztućców. Implementacja rozwiązania zakłada wykorzystanie jednej blokady mutex oraz po jednym semaforze binarnym i jednej zmiennej przechowującej aktualny stan dla każdego z filozofów (wątków).


## Wątki w programie

Każdy filozof w problemie, reprezentowany jest przez wątek (std::thread). W każdym z wątków, w nieskończonej pętli, wykonywana jest następująca sekwencja operacji:
1. filozof myśli,
2. filozof próbuje podnieść widelce,
3. filozof je,
4. filozof odkłada widelce.

Program jako argument przyjmuje liczbę wątków (filozofów), które działają rónwolegle. Główny wątek programu oczekuje na zakończenie wszystkich wątków filozofów, dzięki wywołaniu metody _join()_ dla każdego z nich.


## Sekcje krytyczne

Sekcja krytyczna to fragment kodu, wykorzystujący pewien współdzielony zasób, np. zmienną. W zaimplementowanym rozwiązaniu problemu ucztujących filozofów występują dwie sekcje krytyczne:
1. Modyfikacja tablicy _state_, przechowującej aktualny stan poszczególnych filozofów (wątków)
2. Wyświetlanie w konsoli komunikatów, raportujących o stanie danego wątku

Dostęp do sekcji krytycznych jest chroniony przez obiekty klasy std::mutex - _states_mtx_ i _output_mtx_. Do sekcji krytycznej, modyfikującej zawartość tablicy _state_, może wejść każdy z obecnych wątków filozofów, wywołując metodę _takeForks()_ oraz _putDownForks()_. Druga z sekcji krytycznych także może być osiągnięta przez każdy z działających wątków, dzięki wywołaniu metody _eat()_, _takeForks()_ lub _think()_. Mutexy zapewniają, że w danym momencie, dostęp do współdzielonego zasobu ma co najwyżej jeden wątek.
