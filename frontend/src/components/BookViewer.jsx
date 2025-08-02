import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

const BookViewer = () => {
  const { gutenberg_id } = useParams();
  console.log("gutenberg_id from URL:", gutenberg_id);
  const [chunk, setChunk] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(null);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const fetchChunk = async () => {
      console.log("Fetching:", `${import.meta.env.VITE_API_URL}/book/${gutenberg_id}/chunks?page=${page}&limit=1`);
      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_URL}/book/${gutenberg_id}/chunks?page=${page}&limit=1`,
          {
            headers: {
              "x-api-key": import.meta.env.VITE_API_KEY,
            },
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

  const nextPage = () => setPage((p) => p + 1);
  const prevPage = () => setPage((p) => Math.max(1, p - 1));

  return (
    <div>
      <button onClick={() => navigate("/reader")}>🔙 Back to book list</button>
      <h2>Reading Book #{gutenberg_id || "???"}</h2>

      {error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : (
        <>
          <pre style={{ whiteSpace: "pre-wrap" }}>{chunk}</pre>
          <div style={{ marginTop: "1rem" }}>
            <button onClick={prevPage} disabled={page === 1}>
              Previous
            </button>
            <span style={{ margin: "0 1rem" }}>
              Page {page} {totalPages ? `of ${totalPages}` : ""}
            </span>
            <button
              onClick={nextPage}
              disabled={totalPages ? page >= totalPages : false}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default BookViewer;
