import React, { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "../styles/BookViewer.css";

const BookViewer = () => {
  const { gutenberg_id } = useParams();
  const navigate = useNavigate();

  const storedBook = JSON.parse(localStorage.getItem("selectedBook") || "{}");
  const [chunk, setChunk] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(null);
  const [error, setError] = useState("");
  const [selectedText, setSelectedText] = useState("");
  const [explanation, setExplanation] = useState("");
  const [explaining, setExplaining] = useState(false);
  const [explainError, setExplainError] = useState("");
  const explanationRef = useRef(null); // 🔹 for scroll into view

  useEffect(() => {
    const fetchChunk = async () => {
      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_URL}/book/${gutenberg_id}/chunks?page=${page}&limit=1`,
          {
            headers: { "x-api-key": import.meta.env.VITE_API_KEY },
          }
        );

        if (!res.ok) throw new Error("Failed to fetch chunk");

        const data = await res.json();
        if (!data.chunk || !data.chunk.text) {
          throw new Error("No text found in chunk");
        }

        setChunk(data.chunk.text);
        setTotalPages(data.total_pages || null);
        setError("");
      } catch (err) {
        console.error(err);
        setError("Unable to load this page.");
      }
    };

    fetchChunk();
  }, [gutenberg_id, page]);

  useEffect(() => {
    if (explanationRef.current) {
      explanationRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [explanation, explaining]); // scroll on load or finish

  const nextPage = () => setPage((p) => p + 1);
  const prevPage = () => setPage((p) => Math.max(1, p - 1));

  const fetchExplanation = async (text) => {
    const selected = text.trim();
    const selectedWordCount = selected.split(/\s+/).length;

    if (!selected || selectedWordCount > 50) {
      setExplainError("Please select fewer than 50 words.");
      return;
    }

    const joinedChunk = chunk.replace(/\s+/g, " ");
    const index = joinedChunk.indexOf(selected);
    if (index === -1) {
      setExplainError("Could not locate selected text in chunk.");
      return;
    }

    const before = joinedChunk.slice(0, index).trim().split(/\s+/).slice(-50).join(" ");
    const after = joinedChunk.slice(index + selected.length).trim().split(/\s+/).slice(0, 50).join(" ");

    setExplaining(true);
    setExplainError("");
    setExplanation("");

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/explain`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": import.meta.env.VITE_API_KEY,
        },
        body: JSON.stringify({
          text: selected,
          language_level: "B2",
          book_title: storedBook.title || null,
          book_author: storedBook.author || null,
          book_language: storedBook.language || "Spanish",
          context_before: before,
          context_after: after,
        }),
      });

      if (!res.ok) throw new Error("Explanation failed");

      const data = await res.json();
      setExplanation(data.explanation || "No explanation returned.");
    } catch (err) {
      console.error(err);
      setExplainError("Failed to get explanation.");
    } finally {
      setExplaining(false);
    }
  };

  return (
    <div className="book-viewer-container">
      <button
        className="back-button"
        onClick={() => {
          localStorage.removeItem("selectedBook");
          navigate("/reader");
        }}
      >
        Back to book list
      </button>

      <h2 className="book-title">
        {storedBook.title
          ? `${storedBook.title} by ${storedBook.author}`
          : `Reading Book #${gutenberg_id || "???"}`}
      </h2>

      {error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : (
        <>
          <pre
            className="book-text"
            onMouseUp={() => {
              const selection = window.getSelection().toString().trim();
              if (selection) {
                setSelectedText(selection);
                fetchExplanation(selection);
              }
            }}
          >
            {chunk}
          </pre>

          <div className="pagination-controls">
            <button onClick={prevPage} disabled={page === 1}>
              Previous
            </button>
            <span>
              Page {page} {totalPages ? `of ${totalPages}` : ""}
            </span>
            <button
              onClick={nextPage}
              disabled={totalPages ? page >= totalPages : false}
            >
              Next
            </button>
          </div>

          {selectedText && (
            <div className="explanation-box" ref={explanationRef}>
              <p>
                <strong>Explanation for:</strong> <em>{selectedText}</em>
              </p>
              {explaining ? (
                <div className="spinner"></div>
              ) : explainError ? (
                <p style={{ color: "red" }}>{explainError}</p>
              ) : (
                <p>{explanation}</p>
              )}
              <button
                onClick={() => {
                  setSelectedText("");
                  setExplanation("");
                  setExplainError("");
                }}
              >
                Dismiss
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default BookViewer;
