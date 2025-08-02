import React, { useState, useEffect } from "react";
import LanguageSelector from "../components/LanguageSelector";
import LevelSelector from "../components/LevelSelector";
import BookList from "../components/BookList";
import "../styles/Reader.css";
import { useNavigate } from "react-router-dom";

const Reader = () => {
  const [language, setLanguage] = useState("");
  const [level, setLevel] = useState("");
  const [books, setBooks] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (language && level) {
      fetch(`http://localhost:8000/books/${language}/${level}`, {
        headers: {
          "x-api-key": import.meta.env.VITE_API_KEY
        }
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error(`Failed to fetch books: ${res.status}`);
          }
          return res.json();
        })
        .then((data) => {
          if (!Array.isArray(data)) {
            console.error("Unexpected data format:", data);
            return;
          }
          const filtered = data.filter(
            (book) =>
              book.language.toLowerCase() === language.toLowerCase() &&
              book.language_level.toUpperCase() === level.toUpperCase()
          );
          setBooks(filtered);
        })
        .catch((err) => {
          console.error("Fetch error:", err);
          setBooks([]);
        });
    }
  }, [language, level]);

  return (
    <div className="reader-container">
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>
      <h1 className="reader-heading">Select a Book</h1>

      <div className="selectors-container">
        <LanguageSelector language={language} setLanguage={setLanguage} />
        {language && (
          <LevelSelector language={language} level={level} setLevel={setLevel} />
        )}
      </div>

      {language && level && <BookList books={books} />}
    </div>
  );
};

export default Reader;
