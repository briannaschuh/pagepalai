import React, { useState, useEffect } from "react";
import LanguageSelector from "../components/LanguageSelector";
import LevelSelector from "../components/LevelSelector";
import BookList from "../components/BookList";
import "../styles/Reader.css";

const Reader = () => {
  const [language, setLanguage] = useState("");
  const [level, setLevel] = useState("");
  const [books, setBooks] = useState([]);

  useEffect(() => {
    // fetch only when both selected
    if (language && level) {
      fetch("http://localhost:8000/books", {
        headers: { "x-api-key": "your-api-key-here" } // replace if protected
      })
        .then((res) => res.json())
        .then((data) => {
          const filtered = data.filter(
            (book) =>
              book.language.toLowerCase() === language.toLowerCase() &&
              book.language_level.toUpperCase() === level.toUpperCase()
          );
          setBooks(filtered);
        });
    }
  }, [language, level]);

  return (
    <div className="reader-container">
      <h1>Select a Book</h1>
      <LanguageSelector language={language} setLanguage={setLanguage} />
      {language && (
        <LevelSelector level={level} setLevel={setLevel} />
      )}
      {language && level && <BookList books={books} />}
    </div>
  );
};

export default Reader;
