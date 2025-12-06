import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
import csv

DB_PATH = Path(__file__).resolve().parent / "ssa_names.db"

@dataclass
class NameStat:
    Id: Optional[int]
    Name: str
    Sex: str
    Count: int
    Year: int

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS NameStats (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Sex TEXT NOT NULL,
            Count INTEGER NOT NULL,
            Year INTEGER NOT NULL
        )
        """)
        conn.commit()

def create_name_stat(ns: NameStat) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO NameStats (Name, Sex, Count, Year) VALUES (?, ?, ?, ?)",
            (ns.Name, ns.Sex, ns.Count, ns.Year)
        )
        conn.commit()
        return cur.lastrowid

def get_name_stat_by_id(ns_id: int) -> Optional[NameStat]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM NameStats WHERE Id = ?", (ns_id,)).fetchone()
        return NameStat(**row) if row else None

def list_name_stats(year: Optional[int] = None, limit: int = 20) -> List[NameStat]:
    with get_conn() as conn:
        if year:
            rows = conn.execute(
                "SELECT * FROM NameStats WHERE Year=? ORDER BY Count DESC LIMIT ?",
                (year, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM NameStats ORDER BY Year, Count DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [NameStat(**r) for r in rows]

def update_name_stat(ns: NameStat) -> bool:
    if ns.Id is None:
        raise ValueError("update_name_stat requires Id")
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE NameStats SET Name=?, Sex=?, Count=?, Year=? WHERE Id=?",
            (ns.Name, ns.Sex, ns.Count, ns.Year, ns.Id)
        )
        conn.commit()
        return cur.rowcount == 1

def delete_name_stat(ns: NameStat) -> bool:
    if ns.Id is None:
        raise ValueError("delete_name_stat requires Id")
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM NameStats WHERE Id=?", (ns.Id,))
        conn.commit()
        return cur.rowcount == 1

def load_ssa_file(filename: str):
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File '{filename}' not found.")
    year = int(file_path.stem[-4:])
    with get_conn() as conn:
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 3:
                    continue
                name, sex, count = row
                conn.execute(
                    "INSERT INTO NameStats (Name, Sex, Count, Year) VALUES (?, ?, ?, ?)",
                    (name, sex, int(count), year)
                )
        conn.commit()

def load_all_ssa_files(folder_path: str):
    folder = Path(folder_path)
    for file_path in folder.glob("*.txt"):
        load_ssa_file(file_path)

def list_name_stats_dict(year: Optional[int] = None, limit: int = 20) -> List[dict]:
    return [ns.__dict__ for ns in list_name_stats(year, limit)]

def get_name_stat_by_id_dict(ns_id: int) -> Optional[dict]:
    ns = get_name_stat_by_id(ns_id)
    return ns.__dict__ if ns else None

def create_name_stat_dict(name: str, sex: str, count: int, year: int) -> int:
    ns = NameStat(Id=None, Name=name, Sex=sex, Count=count, Year=year)
    return create_name_stat(ns)
