import os
from sqlalchemy import create_engine, text
from backend.reference.constants import LANGS, LEVELS

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)

if __name__ == "__main__":
    with engine.begin() as conn:
        # language_mapping
        conn.execute(text("""
            INSERT INTO language_mapping (code, name) VALUES
            (:es_code, :es_name), (:pt_code, :pt_name)
            ON CONFLICT (code) DO UPDATE SET name = EXCLUDED.name
        """), {"es_code":"es","es_name":"Spanish","pt_code":"pt","pt_name":"Portuguese"})

        # language_levels (all combos)
        values = []
        params = {}
        i = 0
        for code, _ in LANGS:
            for lvl in LEVELS:
                i += 1
                values.append(f"(:lang{i}, :lvl{i})")
                params[f"lang{i}"] = code
                params[f"lvl{i}"] = lvl
        conn.execute(text(f"""
            INSERT INTO language_levels (language, level)
            VALUES {", ".join(values)}
            ON CONFLICT (language, level) DO NOTHING
        """), params)

    print("Seeded language_mapping and language_levels")
