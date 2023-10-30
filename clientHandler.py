from dataStructures import Book

def handle_client(client_socket, shared_list, list_lock, connection_order_lock, connection_order_container):
    global connection_order

    data_buffer = ""  # Buffer to store incoming data
    current_book = None  # To track the current book being received

    while True:
        data = client_socket.recv(1024)

        if not data:
            print(f"Connection closed. Remaining data_buffer: {data_buffer}")
            break  # Client has closed the connection

        data_buffer += data.decode('utf-8')

        # Check for end of message
        while "\n" in data_buffer:
            line, data_buffer = data_buffer.split("\n", 1)  # Extract the first line

            # if current_book:
            #     print(f"Current book title: {current_book.header.line}")

            # If it's the start of a new book
            if current_book is None:
                current_book = Book(line)  # Create a new book with the title
            else:
                current_book.add_line(line)  # Add the line to the current book's lines
                print(f"Added line: {line}")

        # If the book is complete ....
        if current_book and (not data or "###END_OF_BOOK###" in data_buffer):
            print("Book received and added to shared list.")
            with list_lock:
                shared_list.add_book(current_book)

    # Write the received book to a file
        with connection_order_lock:
            print(f"Before update: {connection_order_container[0]}")  # Debug print
            connection_order_container[0] += 1
            print(f"After update: {connection_order_container[0]}")  # Debug print
            filename = f"book_{connection_order_container[0]:02}.txt"

    try:
        with open(filename, 'w') as file:
            print(f"Attempting to write to {filename}")
            current_node = current_book.header
            while current_node:
                file.write(current_node.line + "\n")
                current_node = current_node.next
        print(f"Book written to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")

    client_socket.send(b"ACK")
    client_socket.close()
