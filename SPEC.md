# Specificatii aplicatie TODO CLI

Aplicatia trebuie sa fie scrisa in Python si sa ruleze in terminal (REPL) dintr-un fisier numit todo.py.
Trebuie sa salveze sarcinile intr-un fisier JSON local, numit 'tasks.json' pentru a nu le pierde la inchidere.

## Functionalitati cerute:
1. **Adaugare sarcina:** Adauga o sarcina cu un text si o seteaza implicit ca nefinalizata.
2. **Listare sarcini:** Afiseaza toate sarcinile salvate, cu un index numeric si statusul lor: [ ] sau [X], [ ] fiind NEFINALIZATA, iar [X] FINALIZATA.
3. **Marcheaza ca rezolvata:** Primeste indexul sarcinii si ii schimba statusul din nefinalizata in finalizata.
4. **Stergere sarcina:** Primeste indexul sarcinii si o sterge din lista.
5. **Iesire:** Inchide aplicatia de tip REPL.
