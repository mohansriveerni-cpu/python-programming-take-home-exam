class Book:

    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False

        return (
            self.title == other.title
            and self.author == other.author
        )

    def age(self, current_year):
        return current_year - self.year


class EBook(Book):

    def __init__(self, title, author, year, size_mb):
        super().__init__(title, author, year)
        self.size_mb = size_mb

    def __str__(self):
        return (
            f"{self.title} by {self.author} "
            f"({self.year}) - {self.size_mb} MB"
        )

    def download_seconds(self, mbit_per_s):
        size_in_megabits = self.size_mb * 8
        seconds = size_in_megabits / mbit_per_s

        return round(seconds, 1)


class Library:

    def __init__(self):
        self.books = []

    def add(self, book):
        if book not in self.books:
            self.books.append(book)

    def find_by_author(self, author) -> list:
        return [
            book for book in self.books
            if book.author == author
        ]

    def oldest(self) -> Book:
        return min(self.books, key=lambda book: book.year)

    def __len__(self):
        return len(self.books)


# Demo
if __name__ == "__main__":

    book1 = Book("1984", "George Orwell", 1949)
    book2 = Book("Dune", "Frank Herbert", 1965)
    book3 = Book("The Hobbit", "J.R.R. Tolkien", 1937)

    ebook1 = EBook(
        "Clean Code",
        "Robert C. Martin",
        2008,
        5.0
    )

    ebook2 = EBook(
        "Python Crash Course",
        "Eric Matthes",
        2019,
        8.0
    )

    duplicate = Book(
        "1984",
        "George Orwell",
        2000
    )

    library = Library()

    library.add(book1)
    library.add(book2)
    library.add(book3)
    library.add(ebook1)
    library.add(ebook2)

    # Duplicate should be ignored
    library.add(duplicate)

    print("Library length:", len(library))

    print("\nBooks:")
    for book in library.books:
        print(book)

    print("\nBook age:")
    print(book1.age(2026))

    print("\nEquality:")
    print(book1 == duplicate)

    print("\nBooks by George Orwell:")
    print(library.find_by_author("George Orwell"))

    print("\nOldest book:")
    print(library.oldest())

    print("\nEBook download time:")
    print(ebook1.download_seconds(10))
