with open("test.bin", "rb+") as file:
    file.seek(7)
    file.write(b' dodaje tekst binarnie ')