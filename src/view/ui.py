import src.controller.control as control


def start():
    choice = None

    print("Choose one of the following options:\n"
          "-> 1: Generate Key\n"
          "-> 2: Encrypt Text\n"
          "-> 3: Decrypt Text\n"
          "-> 4: Leave\n")

    files_dir = control.get_files_dir()

    while choice != "4":
        choice = input("-> ")

        match choice:
            case "1":
                control.generate_key(files_dir)
            case "2":
                control.encrypt_plaintext(files_dir)
            case "3":
                control.decrypt_text(files_dir)
            case "4":
                return
            case _:
                print("Invalid choice, try again!\n")