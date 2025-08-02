import React from "react";
import { useNavigate } from "react-router-dom";

const BookList = ({ books }) => {
  const navigate = useNavigate();

  return (
    <div>
      <h2>Books Available:</h2>
      {books.length === 0 ? (
        <p>No books found for that level and language.</p>
      ) : (
        <ul>
          {books.map((book) => (
            <li
              key={book.id}
              style={{ cursor: "pointer" }}
              onClick={() => {
                console.log("Book object being clicked:", book); 
                navigate(`/reader/${book.gutenberg_id}`);    
              }}
            >
              <strong>{book.title}</strong> by {book.author}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default BookList;
