import React, { useEffect, useState } from "react";

const LevelSelector = ({ level, setLevel, language }) => {
  const [levels, setLevels] = useState([]);

  useEffect(() => {
    console.log("🔁 useEffect triggered in LevelSelector");
    console.log("🧠 language passed to LevelSelector:", language);
  }, [language]);
  
  
  useEffect(() => {
    console.log("Language changed in LevelSelector:", language);
    const fetchLevels = async () => {
      if (!language) return; // no call if language isn't selected

      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_URL}/levels/${language}`,
          {
            headers: {
              "x-api-key": import.meta.env.VITE_API_KEY,
            },
          }
        );

        if (!res.ok) throw new Error("Failed to fetch levels");

        const data = await res.json();
        console.log("Levels response:", data); // debugging
        setLevels(data);
      } catch (err) {
        console.error("Error fetching levels:", err);
        setLevels([]); // fallback to empty if error
      }
    };

    fetchLevels(); // re-fetch whenver language changes
  }, [language]);

  return (
    <div>
      <label>Select a Level:</label>
      <select value={level} onChange={(e) => setLevel(e.target.value)}>
        <option value="">-- Choose --</option>
        {levels.map((lvlObj) => (
          <option key={lvlObj.level} value={lvlObj.level}>
            {lvlObj.level}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LevelSelector;
