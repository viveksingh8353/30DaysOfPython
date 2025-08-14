
from __future__ import annotations
from typing import Dict, List, Set

# ──────────────────────────────────────────────────────────────
# Base Class: Book (Constructor + Encapsulation)
# ──────────────────────────────────────────────────────────────
class Book:
    def __init__(self, title: str, author: str, genre: str = "General", copies: int = 1):
        # public
        self.title = title.strip().title()
        self.author = author.strip().title()
        self.genre = genre.strip().title()
        # private (encapsulation)
        self.__copies = max(0, int(copies))

    
    @property
    def copies(self) -> int:
        return self.__copies

    @copies.setter
    def copies(self, value: int) -> None:
        if value < 0:
            raise ValueError("Copies cannot be negative.")
        self.__copies = int(value)

    def borrow(self) -> bool:
        """Borrow one copy if available."""
        if self.__copies > 0:
            self.__copies -= 1
            return True
        return False

    def return_copy(self) -> None:
        self.__copies += 1

    def kind(self) -> str:
        return "Book"

    def __str__(self) -> str:
        return f"[{self.kind()}] {self.title} by {self.author} | Genre: {self.genre} | Copies: {self.copies}"


# ──────────────────────────────────────────────────────────────
# Inheritance: EBook & PrintedBook (override + super())
# ──────────────────────────────────────────────────────────────
class EBook(Book):
    def __init__(self, title: str, author: str, file_format: str = "PDF", size_mb: float = 1.0, copies: int = 1):
        super().__init__(title, author, "Ebook", copies)
        self.file_format = file_format.upper()
        self.size_mb = float(size_mb)

    def kind(self) -> str:
        return "EBook"

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Format: {self.file_format}, Size: {self.size_mb}MB"


class PrintedBook(Book):
    def __init__(self, title: str, author: str, pages: int, weight_grams: int, copies: int = 1):
        super().__init__(title, author, "Printed", copies)
        self.pages = int(pages)
        self.weight_grams = int(weight_grams)

    def kind(self) -> str:
        return "PrintedBook"

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Pages: {self.pages}, Weight: {self.weight_grams}g"


# ──────────────────────────────────────────────────────────────
# Library Manager (uses dict + set)
# ──────────────────────────────────────────────────────────────
class Library:
    def __init__(self) -> None:
        self._books: Dict[int, Book] = {}
        self._next_id: int = 1

    def add_book(self, book: Book) -> int:
        bid = self._next_id
        self._books[bid] = book
        self._next_id += 1
        return bid

    def list_books(self) -> List[str]:
        if not self._books:
            return ["(no books yet)"]
        lines = []
        for bid, book in self._books.items():
            lines.append(f"ID {bid}: {book}")
        return lines

    def search(self, keyword: str) -> List[str]:
        k = keyword.strip().lower()
        matches = []
        for bid, book in self._books.items():
            if (k in book.title.lower()) or (k in book.author.lower()) or (k in book.genre.lower()):
                matches.append(f"ID {bid}: {book}")
        return matches or [f"(no match for '{keyword}')"]

    def borrow(self, bid: int) -> str:
        book = self._books.get(bid)
        if not book:
            return "Invalid ID."
        ok = book.borrow()
        return f"Borrowed: {book.title}" if ok else "No copies available."

    def return_book(self, bid: int) -> str:
        book = self._books.get(bid)
        if not book:
            return "Invalid ID."
        book.return_copy()
        return f"Returned: {book.title}"

    def delete(self, bid: int) -> str:
        if bid in self._books:
            title = self._books[bid].title
            del self._books[bid]
            return f"Deleted: {title}"
        return "Invalid ID."

    
    def stats(self) -> str:
        total_titles = len(self._books)
        total_copies = sum(b.copies for b in self._books.values())
        authors: Set[str] = {b.author for b in self._books.values()}
        genres: Set[str] = {b.genre for b in self._books.values()}
        return (
            f"Total Titles: {total_titles}\n"
            f"Total Copies: {total_copies}\n"
            f"Unique Authors: {len(authors)}\n"
            f"Genres: {', '.join(sorted(genres)) if genres else '-'}"
        )


# ──────────────────────────────────────────────────────────────
# Simple CLI
# ──────────────────────────────────────────────────────────────
def menu() -> None:
    lib = Library()

    while True:
        print("\n=== Library Menu ===")
        print("1) Add PrintedBook")
        print("2) Add EBook")
        print("3) List all books")
        print("4) Search (title/author/genre)")
        print("5) Borrow by ID")
        print("6) Return by ID")
        print("7) Delete by ID")
        print("8) Stats")
        print("9) Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            pages = input("Pages: ").strip() or "100"
            weight = input("Weight (grams): ").strip() or "300"
            copies = input("Copies: ").strip() or "1"
            bid = lib.add_book(PrintedBook(title, author, int(pages), int(weight), int(copies)))
            print(f"Added PrintedBook with ID {bid}")

        elif choice == "2":
            title = input("Title: ")
            author = input("Author: ")
            file_format = input("Format (PDF/EPUB/MOBI): ").strip() or "PDF"
            size = input("Size (MB): ").strip() or "1.0"
            copies = input("Copies: ").strip() or "1"
            bid = lib.add_book(EBook(title, author, file_format, float(size), int(copies)))
            print(f"Added EBook with ID {bid}")

        elif choice == "3":
            print("\n".join(lib.list_books()))

        elif choice == "4":
            kw = input("Keyword: ")
            print("\n".join(lib.search(kw)))

        elif choice == "5":
            bid = int(input("Book ID to borrow: "))
            print(lib.borrow(bid))

        elif choice == "6":
            bid = int(input("Book ID to return: "))
            print(lib.return_book(bid))

        elif choice == "7":
            bid = int(input("Book ID to delete: "))
            print(lib.delete(bid))

        elif choice == "8":
            print(lib.stats())

        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()
