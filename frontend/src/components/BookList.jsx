import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Reader.css";

const BookList = ({ books }) => {
  const navigate = useNavigate();

  const handleBookClick = (book) => {
    localStorage.setItem("selectedBook", JSON.stringify(book));
    navigate(`/reader/${book.gutenberg_id}`);
  };

  return (
    <div className="book-list">
      <h2>Books Available:</h2>
      {books.length === 0 ? (
        <p>No books found for that level and language.</p>
      ) : (
        books.map((book) => (
          <div
            key={book.id}
            className="book-item"
            onClick={() => handleBookClick(book)}
            style={{ cursor: "pointer" }}
          >
            <div className="book-title">{book.title}</div>
            <div className="book-author">by {book.author}</div>
          </div>
        ))
      )}
    </div>
  );
};

export default BookList;
