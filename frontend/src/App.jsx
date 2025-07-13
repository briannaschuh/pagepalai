import React, { useState, useEffect } from "react";
import LanguageSelector from "./components/LanguageSelector";
import LevelSelector from "./components/LevelSelector";
import BookList from "./components/BookList";

const App = () => {
  const [language, setLanguage] = useState("");
  const [level, setLevel] = useState("");
  const [books, setBooks] = useState([]);
  const [error, setError] = useState("");

  // fetch books whenever language or level changes
  useEffect(() => {
    const fetchBooks = async () => {
      if (!language || !level) return;

      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_URL}/books/${language}/${level}`,
          {
            headers: {
              "x-api-key": import.meta.env.VITE_API_KEY,
            },
          }
        );

        if (res.status === 404) {
          setBooks([]);
          setError(""); // no books found but not an error
          return;
        }

        if (!res.ok) throw new Error("Failed to fetch books");

        const data = await res.json();
        setBooks(data);
        setError("");
      } catch (err) {
        console.error(err);
        setBooks([]);
        setError("Something went wrong. Please try again.");
      }
    };

    fetchBooks();
  }, [language, level]);

  return (
    <div className="app-container">
      <h1>📚 PagePal</h1>

      <LanguageSelector
        language={language}
        setLanguage={(lang) => {
          setLanguage(lang);
          setLevel("");
          setBooks([]);
          setError("");
        }}
      />

      {language && (
        <LevelSelector
          language={language}
          level={level}
          setLevel={(lvl) => {
            setLevel(lvl);
            setBooks([]);
            setError("");
          }}
        />
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {language && level && !error && books.length === 0 && (
        <p>No books found for that level and language.</p>
      )}

      {language && level && books.length > 0 && <BookList books={books} />}
    </div>
  );
};

export default App;
