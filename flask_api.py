from flask import Flask, request, jsonify
from database import get_conn  # uses DB_PATH and NameStats in ssa_names.db

app = Flask(__name__)

@app.get("/nameinfo")
def name_info():
    # Get the name from the query string
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Missing 'name' query parameter"}), 400

    name = name.strip()

    # Query the database for yearly totals for the name
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT Year, SUM(Count) AS total
        FROM NameStats
        WHERE Name = ?
        GROUP BY Year
        ORDER BY Year ASC
        """,
        (name,)
    )
    rows = cur.fetchall()

    # No data found for the name
    if not rows:
        return jsonify({"name": name, "error": "Name not found"}), 404

    first_year = rows[0]["Year"]

    most_popular_row = max(rows, key=lambda r: r["total"])
    most_popular_year = most_popular_row["Year"]
  
    sorted_by_popularity = sorted(rows, key=lambda r: r["total"], reverse=True)
    top_years = [r["Year"] for r in sorted_by_popularity[:10]]

    return jsonify({
        "name": name,
        "first_year": first_year,
        "most_popular_year": most_popular_year,
        "top_years": top_years
    })

if __name__ == "__main__":
    app.run(debug=True)
