import React from "react";

const BookList = ({ books }) => {
  return (
    <div>
      <h2>Books Available:</h2>
      {books.length === 0 ? (
        <p>No books found for that level and language.</p>
      ) : (
        <ul>
          {books.map((book) => (
            <li key={book.id}>
              <strong>{book.title}</strong> by {book.author}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default BookList;
