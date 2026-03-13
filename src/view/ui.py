import os
from pathlib import Path
import src.model.cipher as cipher


def start_ui():
    src_dir = Path("ui.py").resolve().parents[2]
    choice = None
    files_dir = f"{src_dir}\\files"

    print("Choose one of the following options:\n"
          "-> 1: Generate Key\n"
          "-> 2: Encrypt Text\n"
          "-> 3: Decrypt Text\n"
          "-> 4: Leave\n")

    if not os.path.exists(files_dir):
        os.makedirs(files_dir)

    while choice != "4":
        choice = input("-> ")

        match choice:
            case "1":
                key_path = os.path.join(files_dir, "key.txt")
                with open(key_path, "w") as file:
                    file.write(cipher.generate_key())
                    file.close()
                print("Key generated on a file, store it on a safe place for it to be used again.")
            case "2":
                try:
                    plaintext_path = os.path.join(files_dir, "plaintext.txt")
                    with open(plaintext_path, "r", encoding='utf-8') as file:
                        clear_text = file.readlines()
                        file.close()
                    print(clear_text)
                except FileNotFoundError:
                    print(f"File not found in \"files\" directory")
            case "3":
                pass
            case "4":
                return
            case _:
                print("Invalid choice, try again!\n")


start_ui()