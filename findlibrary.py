import csv
import os
import re

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nTekan ENTER untuk melanjutkan...")

def splash_screen():
    clear_screen()
    print(r"""
███████╗██╗███╗   ██╗██████╗ ██╗     ██╗██████╗ ██████╗  █████╗ ██████╗ ██╗   ██╗
██╔════╝██║████╗  ██║██╔══██╗██║     ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
█████╗  ██║██╔██╗ ██║██║  ██║██║     ██║██████╔╝██████╔╝███████║██████╔╝ ╚████╔╝ 
██╔══╝  ██║██║╚██╗██║██║  ██║██║     ██║██╔══██╗██╔══██╗██╔══██║██╔══██╗  ╚██╔╝  
██║     ██║██║ ╚████║██████╔╝███████╗██║██████╔╝██║  ██║██║  ██║██║  ██║   ██║   
╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
    """)
    print("SISTEM REKOMENDASI BUKU PERPUSTAKAAN")
    print("UNIVERSITAS JEMBER")
    pause()


def valid_email_mahasiswa(email):
    pattern = r'^\d{12}@mail\.unej\.ac\.id$'
    return re.match(pattern, email)


def login_menu():
    while True:
        clear_screen()
        print("=========== LOGIN ===========")
        print("1. Login Admin")
        print("2. Login Mahasiswa")
        print("0. Kembali ke FindLibrary")
        pilih = input("\nPilih menu: ").strip()

        if pilih == "1":
            return login_admin()
        elif pilih == "2":
            return login_mahasiswa()
        elif pilih == "0":
            return "back"
        else:
            print("Pilihan tidak valid!")
            pause()

def login_admin():
    clear_screen()
    print("====== LOGIN ADMIN ======")
    email = input("Email admin: ").strip().lower()
    password = input("Password   : ").strip()

    if email == "admin@perpus.com" and password == "admin123":
        return "admin"
    else:
        print("Login admin gagal!")
        pause()
        return None

def login_mahasiswa():
    clear_screen()
    print("====== LOGIN MAHASISWA ======")
    print("Format: 12digit@mail.unej.ac.id\n")

    email = input("Email kampus: ").strip().lower()

    if email == "":
        print("Email tidak boleh kosong!")
        return None

    if not valid_email_mahasiswa(email):
        print("Email TIDAK valid!")
        print("Contoh benar: 202210370311@mail.unej.ac.id")
        return None

    return "mahasiswa"

#isi
class Book:
    def __init__(self, title, genre, theme, rating):
        self.title = title
        self.genre = genre
        self.theme = theme
        self.rating = rating

    def __str__(self):
        return f"{self.title} | Genre: {self.genre} | Tema: {self.theme} | Rating: {self.rating}"


def print_table(headers, rows, title=None, table_only=False):
    if not table_only:
        clear_screen()
    if title:
        print(title)
        print("=" * len(title))
    if not rows:
        print("\n( Tidak ada data untuk ditampilkan )")
        return
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, item in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(item)))
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print("\n" + header_row)
    print("-" * len(header_row))
    for row in rows:
        print(" | ".join(str(item).ljust(col_widths[i]) for i, item in enumerate(row)))
    print("-" * len(header_row))

def print_menu(title, rows):
    clear_screen()
    col1_width = 4
    col2_width = max(len(row[1]) for row in rows)
    col2_width = max(col2_width, 20)
    total_width = col1_width + col2_width + 7
    print("+" + "-" * (total_width - 2) + "+")
    print("|" + title.center(total_width - 2) + "|")
    print("+" + "-" * (total_width - 2) + "+")
    print("+" + "-" * col1_width + "+" + "-" * (col2_width + 2) + "+")
    print("| No".ljust(col1_width + 2) + "| " + "MENU".ljust(col2_width) + " |")
    print("+" + "-" * col1_width + "+" + "-" * (col2_width + 2) + "+")
    for no, menu in rows:
        print("| " + str(no).ljust(col1_width - 1) + "| " + menu.ljust(col2_width) + " |")
    print("+" + "-" * col1_width + "+" + "-" * (col2_width + 2) + "+")

#luar
class Node:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None

#bst
class BST:
    def __init__(self):
        self.root = None

    def insert(self, book):
        self.root = self._insert(self.root, book)

    def _insert(self, node, book):
        if node is None:
            return Node(book)
        if book.rating < node.book.rating:
            node.left = self._insert(node.left, book)
        else:
            node.right = self._insert(node.right, book)
        return node

    def collect_with_filter(self, filter_fn):
        hasil = []
        self._collect_with_filter(self.root, filter_fn, hasil)
        return hasil

    def _collect_with_filter(self, node, filter_fn, hasil):
        if node:
            self._collect_with_filter(node.left, filter_fn, hasil)
            if filter_fn(node.book):
                hasil.append(node.book)
            self._collect_with_filter(node.right, filter_fn, hasil)

    def search_by_rating(self, rating):
        return self.collect_with_filter(lambda b: b.rating == rating)

    def search_by_title(self, title):
        hasil = self.collect_with_filter(lambda b: b.title.lower() == title.lower())
        return hasil[0] if hasil else None

    def get_max_rating_book(self):
        if self.root is None:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.book

    def rebuild_from_books(self, books):
        self.root = None
        for b in books:
            self.insert(b)

def save_book_to_csv(book, filename="books.csv"):
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["title", "genre", "theme", "rating"])
        writer.writerow([book.title, book.genre, book.theme, book.rating])

def update_book_in_csv(old_title, updated_book, filename="books.csv"):
    rows = []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["title"].lower() == old_title.lower():
                rows.append({
                    "title": updated_book.title,
                    "genre": updated_book.genre,
                    "theme": updated_book.theme,
                    "rating": updated_book.rating
                })
            else:
                rows.append(row)

    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["title", "genre", "theme", "rating"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def load_books_from_csv(bst, filename="books.csv"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                title = row.get("title")
                genre = row.get("genre")
                theme = row.get("theme")
                rating_str = row.get("rating")
                if not title or not rating_str:
                    continue
                try:
                    rating = int(rating_str)
                except ValueError:
                    continue
                book = Book(title, genre, theme, rating)
                bst.insert(book)
                count += 1
        print(f"{count} buku berhasil dimuat dari {filename}.")
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan. Sistem mulai tanpa data awal.")


def admin_menu(bst):
    while True:

        rows = [
            [1, "Tambah Buku"],
            [2, "Lihat Semua Buku"],
            [3, "Cari Buku"],
            [4, "Ubah Buku"],
            [5, "Hapus Buku"],
            [6, "Logout"]
        ]

        print_menu("HALAMAN ADMIN", rows)

        pilih = input("\nPilih menu: ").strip()

        if pilih == "1":
            tambah_buku(bst)
        elif pilih == "2":
            lihat_semua_buku(bst)
        elif pilih == "3":
            admin_cari_buku(bst)
        elif pilih == "4":
            ubah_buku(bst)
        elif pilih == "5":
            hapus_buku(bst)
        elif pilih == "6":
            break
        else:
            print("Pilihan tidak valid.")
            pause()


def tambah_buku(bst):
    clear_screen()
    print("=== TAMBAH BUKU ===")
    title = input("Judul : ").strip()
    genre = input("Genre : ").strip()
    theme = input("Tema  : ").strip()
    try:
        rating = int(input("Rating (1-10): ").strip())
    except ValueError:
        print("Rating harus berupa angka.")
        pause()
        return
    
    book = Book(title, genre, theme, rating)
    bst.insert(Book(title, genre, theme, rating))
    save_book_to_csv(Book(title, genre, theme, rating))
    print("\nBuku berhasil ditambahkan!")


def lihat_semua_buku(bst):
    semua = bst.collect_with_filter(lambda b: True)
    rows = [[i+1, b.title, b.genre, b.theme, b.rating] for i, b in enumerate(semua)]
    print_table(["No", "Judul", "Genre", "Tema", "Rating"], rows, "DAFTAR SEMUA BUKU")

def admin_cari_buku(bst):
    while True:
        clear_screen()
        print("=== CARI BUKU (ADMIN) ===")
        print("1. Berdasarkan Judul")
        print("2. Berdasarkan Rating")
        print("3. Kembali")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            judul = input("Masukkan judul buku: ").strip()
            buku = bst.search_by_title(judul)
            if buku:
                rows = [[buku.title, buku.genre, buku.theme, buku.rating]]
                print_table(["Judul", "Genre", "Tema", "Rating"], rows, "BUKU DITEMUKAN")
            else:
                print("\nBuku tidak ditemukan.")

        elif pilih == "2":
            try:
                rating = int(input("Masukkan rating: ").strip())
            except ValueError:
                print("Rating harus angka.")
                continue
            hasil = bst.search_by_rating(rating)
            if hasil:
                rows = [[i+1, b.title, b.genre, b.theme, b.rating]
                        for i, b in enumerate(hasil)]
                print_table(["No", "Judul", "Genre", "Tema", "Rating"],
                            rows, f"BUKU DENGAN RATING {rating}")
            else:
                print("\nTidak ada buku dengan rating tersebut.")


        elif pilih == "3":
            break
        else:
            print("Pilihan tidak valid.")



def _collect_all_books(bst):
    return bst.collect_with_filter(lambda b: True)


def ubah_buku(bst):
    clear_screen()
    print("=== UBAH BUKU ===")
    judul = input("Masukkan judul buku yang ingin diubah: ").strip()

    semua = _collect_all_books(bst)
    target = None
    for b in semua:
        if b.title.lower() == judul.lower():
            target = b
            break

    if not target:
        print("\nBuku tidak ditemukan.")
        pause()
        return

    print("\nData lama:")
    print(target)

    new_title = input("\nJudul baru  (kosongkan jika tidak diubah): ").strip()
    new_genre = input("Genre baru  (kosongkan jika tidak diubah): ").strip()
    new_theme = input("Tema baru   (kosongkan jika tidak diubah): ").strip()
    new_rating_str = input("Rating baru (kosongkan jika tidak diubah): ").strip()

    old_title = target.title

    if new_title:
        target.title = new_title
    if new_genre:
        target.genre = new_genre
    if new_theme:
        target.theme = new_theme
    if new_rating_str:
        try:
            target.rating = int(new_rating_str)
        except ValueError:
            print("Rating baru tidak valid, diabaikan.")

    update_book_in_csv(old_title, target)
    bst.rebuild_from_books(semua)
    print("\nData buku berhasil diubah.")


def hapus_buku(bst):
    clear_screen()
    print("=== HAPUS BUKU ===")
    judul = input("Masukkan judul buku yang ingin dihapus: ").strip()

    semua = _collect_all_books(bst)
    baru = []
    found = False
    for b in semua:
        if b.title.lower() == judul.lower() and not found:
            found = True
            continue
        baru.append(b)

    if not found:
        print("\nBuku tidak ditemukan.")
        pause()
        return

    delete_book_from_csv(judul)
    bst.rebuild_from_books(baru)
    print("\nBuku berhasil dihapus.")


def mahasiswa_menu(bst, tbr_list, wishlist):
    while True:

        rows = [
            [1, "Cari Buku"],
            [2, "Lihat Rekomendasi"],
            [3, "To Be Read (TBR)"],
            [4, "Wishlist"],
            [5, "Logout"]
        ]

        print_menu("HALAMAN MAHASISWA", rows)

        pilih = input("\nPilih menu: ").strip()

        if pilih == "1":
            menu_cari_buku_mahasiswa(bst, tbr_list, wishlist)
        elif pilih == "2":
            menu_rekomendasi(bst, tbr_list, wishlist)
        elif pilih == "3":
            menu_tbr(tbr_list)
        elif pilih == "4":
            menu_wishlist(wishlist)
        elif pilih == "5":
            break
        else:
            print("Pilihan tidak valid.")

def menu_cari_buku_mahasiswa(bst, tbr_list, wishlist):
    while True:
        clear_screen()
        print("======== CARI BUKU ========")
        print("1. Rating")
        print("2. Genre")
        print("3. Tema")
        print("4. Rating + Genre")
        print("5. Genre + Tema")
        print("6. Rating + Tema")
        print("7. Rating + Genre + Tema")
        print("8. Kembali")

        pilih = input("Pilih: ").strip()

        def tampil(hasil, judul_tabel):
            rows = [[i+1, b.title, b.genre, b.theme, b.rating]
                    for i, b in enumerate(hasil)]
            print_table(["No", "Judul", "Genre", "Tema", "Rating"], rows, judul_tabel)
            if hasil:
                opsi_simpan(hasil, tbr_list, wishlist)
            else:
                pause()

        if pilih == "1":
            try:
                rating = int(input("Rating: ").strip())
            except ValueError:
                print("Rating harus angka.")
                continue
            hasil = bst.search_by_rating(rating)
            tampil(hasil, f"HASIL PENCARIAN - RATING {rating}")

        elif pilih == "2":
            genre = input("Genre: ").strip().lower()
            hasil = bst.collect_with_filter(lambda b: b.genre.lower() == genre)
            tampil(hasil, f"HASIL PENCARIAN - GENRE {genre}")

        elif pilih == "3":
            tema = input("Tema: ").strip().lower()
            hasil = bst.collect_with_filter(lambda b: b.theme.lower() == tema)
            tampil(hasil, f"HASIL PENCARIAN - TEMA {tema}")

        elif pilih == "4":
            rating = int(input("Minimal rating: "))
            genre = input("Genre: ").strip().lower()
            hasil = bst.collect_with_filter(
                lambda b: b.rating >= rating and b.genre.lower() == genre
            )
            tampil(hasil, f"RATING >= {rating} & GENRE {genre}")

        elif pilih == "5":
            genre = input("Genre: ").strip().lower()
            tema = input("Tema: ").strip().lower()
            hasil = bst.collect_with_filter(
                lambda b: b.genre.lower() == genre and b.theme.lower() == tema
            )
            tampil(hasil, f"GENRE {genre} & TEMA {tema}")

        elif pilih == "6":
            rating = int(input("Minimal rating: "))
            tema = input("Tema: ").strip().lower()
            hasil = bst.collect_with_filter(
                lambda b: b.rating >= rating and b.theme.lower() == tema
            )
            tampil(hasil, f"RATING >= {rating} & TEMA {tema}")

        elif pilih == "7":
            rating = int(input("Minimal rating: "))
            genre = input("Genre: ").strip().lower()
            tema = input("Tema: ").strip().lower()
            hasil = bst.collect_with_filter(
                lambda b: b.rating >= rating and
                          b.genre.lower() == genre and
                          b.theme.lower() == tema
            )
            tampil(hasil, f"RATING >= {rating}, GENRE {genre}, TEMA {tema}")

        elif pilih == "8":
            break
        else:
            print("Pilihan tidak valid.")



def opsi_simpan(hasil, tbr_list, wishlist):
    while True:
        print("\n1. Tambah ke To Be Read")
        print("2. Tambah ke Wishlist")
        print("3. Kembali")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            idx = input("Nomor buku: ").strip()
            if not idx.isdigit() or not (1 <= int(idx) <= len(hasil)):
                print("Nomor tidak valid.")
                continue
            tbr_list.append(hasil[int(idx) - 1])
            print("Ditambahkan ke TBR.")
            pause()
            break

        elif pilih == "2":
            idx = input("Nomor buku: ").strip()
            if not idx.isdigit() or not (1 <= int(idx) <= len(hasil)):
                print("Nomor tidak valid.")
                continue
            wishlist.append(hasil[int(idx) - 1])
            print("Ditambahkan ke Wishlist.")
            pause()
            break

        elif pilih == "3":
            break
        else:
            print("Pilihan tidak valid.")

def delete_book_from_csv(title, filename="books.csv"):
    try:
        rows = []

        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["title"].lower() != title.lower():
                    rows.append(row)

        with open(filename, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["title", "genre", "theme", "rating"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    except FileNotFoundError:
        print("File CSV tidak ditemukan.")

def menu_rekomendasi(bst, tbr_list, wishlist):
    buku = bst.get_max_rating_book()
    clear_screen()
    if not buku:
        print("Tidak ada buku di sistem.")
        pause()
        return

    rows = [[buku.title, buku.genre, buku.theme, buku.rating]]
    print_table(["Judul", "Genre", "Tema", "Rating"], rows, "REKOMENDASI BUKU")

    while True:
        print("\n1. Tambah ke TBR")
        print("2. Tambah ke Wishlist")
        print("3. Kembali")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            tbr_list.append(buku)
            print("Ditambahkan ke TBR.")
            pause()
            break
        elif pilih == "2":
            wishlist.append(buku)
            print("Ditambahkan ke Wishlist.")
            pause()
            break
        elif pilih == "3":
            break
        else:
            print("Pilihan tidak valid.")


def menu_tbr(tbr_list):
    rows = [[i+1, b.title, b.genre, b.theme, b.rating]
            for i, b in enumerate(tbr_list)]
    print_table(["No", "Judul", "Genre", "Tema", "Rating"], rows, "DAFTAR TO BE READ (TBR)")
    pause()


def menu_wishlist(wishlist):
    rows = [[i+1, b.title, b.genre, b.theme, b.rating]
            for i, b in enumerate(wishlist)]
    print_table(["No", "Judul", "Genre", "Tema", "Rating"], rows, "DAFTAR WISHLIST")
    pause()


def main():
    while True:
        splash_screen()
        role = login_menu()

        if role == "back":
            continue
        elif role == "admin":
            admin_menu(bst)
        elif role == "mahasiswa":
            mahasiswa_menu(bst, tbr_list, wishlist)

if __name__ == "__main__":
    bst = BST()
    load_books_from_csv(bst, "books.csv")
    tbr_list = []
    wishlist = []
    main()
