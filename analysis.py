import time

pattern_frequencies = {}

def analysis_thread(shared_list, search_pattern):
    while True:
        # Compute the frequency of the search pattern for each book
        current_book = shared_list.header
        while current_book:
            frequency = current_book.lines.count(search_pattern)
            pattern_frequencies[current_book.title] = frequency
            current_book = current_book.book_next

        # Sort books by pattern frequency and print titles
        sorted_books = sorted(pattern_frequencies.keys(), key=lambda x: pattern_frequencies[x], reverse=True)
        print("Books sorted by pattern frequency:")
        for book in sorted_books:
            print(book)

        # Wait for the specified interval before the next analysis
        time.sleep(5)  # or another interval


def print_books(shared_list_head):
    current_book_header = shared_list_head
    while current_book_header:
        print(f"Book Title: {current_book_header.line}")
        current_node = current_book_header.next
        while current_node and current_node != current_book_header.book_next:
            print(current_node.line)
            current_node = current_node.next
        current_book_header = current_book_header.book_next

