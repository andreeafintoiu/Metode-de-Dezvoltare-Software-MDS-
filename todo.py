import json
import os

FISIER_DATE = "tasks.json"

def incarca_sarcini():
    if not os.path.exists(FISIER_DATE):
        return []
    with open(FISIER_DATE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salveaza_sarcini(sarcini):
    with open(FISIER_DATE, "w") as f:
        json.dump(sarcini, f, indent=4)

def main():
    sarcini = incarca_sarcini()
    
    while True:
        print("\n--- TODO CLI (MDS Project) ---")
        print("1. Adauga sarcina")
        print("2. Listeaza sarcini")
        print("3. Marcheaza ca rezolvata")
        print("4. Sterge sarcina")
        print("5. Iesire")
        
        optiune = input("Alege optiunea: ").strip()
        
        # 1. Adaugare sarcina
        if optiune == "1":
            text = input("\nIntrodu textul sarcinii: ").strip()
            if text:
                sarcini.append({"text": text, "finalizata": False})
                salveaza_sarcini(sarcini)
                print("Sarcina a fost adaugata ca nefinalizata!")
                
        # 2. Listare sarcini
        elif optiune == "2":
            if not sarcini:
                print("\nLista de sarcini este goala.")
            else:
                print("\n=== LISTA SARCINI ===")
                for i, s in enumerate(sarcini, 1):
                    status = "[X]" if s["finalizata"] else "[ ]"
                    print(f"{i}. {status} {s['text']}")
                print("=====================")
                
        # 3. Marcheaza ca rezolvata
        elif optiune == "3":
            if not sarcini:
                print("\nNu exista sarcini in lista.")
                continue
            try:
                idx = int(input("\nIntrodu indexul sarcinii de marcat ca rezolvata: ")) - 1
                if 0 <= idx < len(sarcini):
                    sarcini[idx]["finalizata"] = True
                    salveaza_sarcini(sarcini)
                    print(f"Sarcina '{sarcini[idx]['text']}' a fost marcata ca rezolvata!")
                else:
                    print("Index invalid.")
            except ValueError:
                print("Te rog introdu un numar valid.")
                
        # 4. Stergere sarcina
        elif optiune == "4":
            if not sarcini:
                print("\nNu exista sarcini de sters.")
                continue
            try:
                idx = int(input("\nIntrodu indexul sarcinii pe care vrei sa o stergi: ")) - 1
                if 0 <= idx < len(sarcini):
                    stearsa = sarcini.pop(idx)
                    salveaza_sarcini(sarcini)
                    print(f"Sarcina '{stearsa['text']}' a fost stearsa din lista.")
                else:
                    print("Index invalid.")
            except ValueError:
                print("Te rog introdu un numar valid.")
                
        # 5. Iesire
        elif optiune == "5":
            print("\nAplicatie inchisa. Toate modificarile au fost salvate in tasks.json!")
            break
        else:
            print("\nOptiune invalida. Incearca din nou.")

if __name__ == "__main__":
    main()
