class Book:
    def __init__(self, title, genre, theme, rating):
        self.title = title
        self.genre = genre
        self.theme = theme
        self.rating = rating

class Node:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None

#bst menyimpan bukunya
class BST:
    def __init__(self):
        self.root = None

    #insert buku ke bst -> rating
    def insert(self, book):
        self.root = self._insert(self.root, book)

    def _insert(self, root, book):
        if root is None:
            return Node(book)
        if book.rating < root.book.rating:
            root.left = self._insert(root.left, book)
        else:
            root.right = self._insert(root.right, book)
        return root

    #melihat semua buku
    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(f"Judul: {root.book.title} | Genre: {root.book.genre} | Tema: {root.book.theme} | Rating: {root.book.rating}")
            self.inorder(root.right)

def splash_screen():
    print("====================================")
    print("            FINDLIBRARY")
    print("   Sistem Rekomendasi Buku Perpus")
    print("====================================")
    input("Tekan ENTER untuk melanjutkan...")

#login
def login():
    print("\n=========== LOGIN ===========")
    username = input("Masukkan username: ")
    password = input("Masukkan password (kosongkan jika mahasiswa): ")

    if username == "admin" and password == "admin123":
        print("\nLogin sebagai ADMIN berhasil!\n")
        return "admin"

    if username != "admin":
        print("\nMasuk sebagai MAHASISWA.\n")
        return "mahasiswa"

    print("Login gagal!")
    return None

#admin
def menu_admin(bst):
    while True:
        print("========== HALAMAN ADMIN ==========")
        print("1. Tambah Buku")
        print("2. Lihat Semua Buku")
        print("3. Ubah Buku")
        print("4. Hapus Buku")
        print("5. Logout")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_buku(bst)
        elif pilih == "2":
            print("\n=== DAFTAR SEMUA BUKU ===")
            bst.inorder(bst.root)
            print()
        elif pilih == "3":
            print("Fitur ubah buku belum dibuat.\n")
        elif pilih == "4":
            print("Fitur hapus buku belum dibuat.\n")
        elif pilih == "5":
            break
        else:
            print("Pilihan tidak valid!\n")

#tambah buku - admin
def tambah_buku(bst):
    print("\n=== TAMBAH BUKU ===")
    title = input("Judul: ")
    genre = input("Genre: ")
    theme = input("Tema: ")
    rating = int(input("Rating: "))

    book = Book(title, genre, theme, rating)
    bst.insert(book)

    print("\nBuku berhasil ditambahkan!\n")

#user (mahasiw)
def menu_mahasiswa(bst):
    while True:
        print("========= HALAMAN MAHASISWA =========")
        print("1. Cari Berdasarkan Rating")
        print("2. Cari Berdasarkan Genre")
        print("3. Cari Berdasarkan Tema")
        print("4. Rating + Genre")
        print("5. Genre + Tema")
        print("6. Rating + Tema")
        print("7. Rating + Genre + Tema")
        print("8. Lihat Rekomendasi Buku")
        print("9. Logout")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            print("Fitur cari rating belum dibuat.")
        elif pilih == "2":
            print("Fitur cari genre belum dibuat.")
        elif pilih == "3":
            print("Fitur cari tema belum dibuat.")
        elif pilih == "4":
            print("Fitur kombinasi belum dibuat.")
        elif pilih == "5":
            print("Fitur kombinasi belum dibuat.")
        elif pilih == "6":
            print("Fitur kombinasi belum dibuat.")
        elif pilih == "7":
            print("Fitur kombinasi belum dibuat.")
        elif pilih == "8":
            print("Fitur rekomendasi belum dibuat.")
        elif pilih == "9":
            break
        else:
            print("Pilihan tidak valid!\n")


if __name__ == "__main__":
    bst = BST()
    splash_screen()

    while True:
        role = login()

        if role == "admin":
            menu_admin(bst)
        elif role == "mahasiswa":
            menu_mahasiswa(bst)
        else:
            print("Silakan coba login kembali.\n")
