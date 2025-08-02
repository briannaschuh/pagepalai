import React, { useEffect, useState } from "react";

const LanguageSelector = ({ language, setLanguage }) => {
  const [languages, setLanguages] = useState([]);

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/languages`, {
          headers: {
            "x-api-key": import.meta.env.VITE_API_KEY,
          },
        });

        if (!res.ok) throw new Error("Failed to fetch languages");

        const data = await res.json();
        console.log("Fetched languages:", data);
        setLanguages(data);
      } catch (err) {
        console.error("Language fetch failed:", err);
        setLanguages([]);
      }
    };

    fetchLanguages();
  }, []);

  return (
    <div>
      <label>Select a Language:</label>
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option value="">-- Choose --</option>
        {languages.map((langObj) => (
          <option key={langObj.code} value={langObj.code}>
            {langObj.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelector;
