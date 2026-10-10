# Technical Requirements
## Northpeak Retail Analytics

**Version:** 1.0  
**Date:** October 2026

---

## 1. System Requirements

### 1.1 Operating System
- Windows 10/11, macOS 12+, or Ubuntu 20.04+
- 64-bit architecture required

### 1.2 Hardware (Minimum)
| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 4 GB | 8 GB+ |
| Storage | 2 GB free | 5 GB free |
| CPU | Dual-core | Quad-core |

---

## 2. Software Requirements

### 2.1 Python
- **Version:** Python 3.9 or higher
- **Installer:** [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
```

### 2.2 PostgreSQL
- **Version:** PostgreSQL 13 or higher
- **Installer:** [postgresql.org](https://www.postgresql.org/download/)
- Default port: `5432`
- A database named `northpeak_db` must exist before running the script

Create the database after installing PostgreSQL:
```sql
CREATE DATABASE northpeak_db;
```

### 2.3 Power BI Desktop
- **Version:** Power BI Desktop (latest)
- **Download:** [Microsoft Power BI](https://powerbi.microsoft.com/desktop/)
- Required to open the `.pbix` dashboard file
- **Note:** Power BI Desktop is Windows-only. Mac users can use Power BI in a browser (limited) or run it via a virtual machine.

### 2.4 Jupyter Notebook (Optional)
- Included in the `requirements.txt` dependencies
- Required only to re-run or explore the analysis notebook
- Alternative: use VS Code with the Jupyter extension

---

## 3. Python Package Requirements

All packages are listed in `requirements.txt`. Install with:

```bash
pip install -r requirements.txt
```

### 3.1 Package Details

| Package | Version | Purpose |
|---------|---------|---------|
| `psycopg2-binary` | 2.9.9 | PostgreSQL database adapter for Python |
| `SQLAlchemy` | 2.0.23 | ORM and database connection engine |
| `pandas` | 2.1.4 | Data manipulation and `.to_sql()` bulk inserts |
| `numpy` | 1.26.2 | Vectorized math for financial computations |
| `matplotlib` | 3.8.2 | Base plotting library for notebook charts |
| `seaborn` | 0.13.0 | Statistical data visualization on top of matplotlib |
| `python-dotenv` | 1.0.0 | Load credentials from `.env` file |
| `jupyter` | 1.0.0 | Jupyter Notebook server |
| `ipykernel` | 6.27.1 | Jupyter kernel for Python |

---

## 4. Environment Configuration

### 4.1 Environment Variables

The project uses a `.env` file to store sensitive credentials. Never commit this file to version control.

**Setup steps:**
1. Copy `.env.example` to `.env`
2. Fill in your actual database credentials

```bash
# .env.example structure
DB_HOST=localhost
DB_PORT=5432
DB_NAME=northpeak_db
DB_USER=your_username
DB_PASS=your_password
```

### 4.2 Virtual Environment (Recommended)

Isolate project dependencies with a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows CMD)
venv\Scripts\activate

# Activate (Windows PowerShell)
venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 5. PostgreSQL Setup

### 5.1 Database Creation
```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create the database
CREATE DATABASE northpeak_db;

-- Verify
\l
```

### 5.2 User Permissions
The PostgreSQL user specified in `.env` needs the following privileges on `northpeak_db`:
- `CREATE` — to create tables and indexes
- `INSERT` — to load data
- `SELECT` — to query data

```sql
-- Grant necessary permissions (run as postgres superuser)
GRANT ALL PRIVILEGES ON DATABASE northpeak_db TO your_username;
```

### 5.3 Connection Test
You can verify the connection before running the script:
```python
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
with engine.connect() as conn:
    print(conn.execute(text("SELECT version()")).fetchone())
```

---

## 6. Running the Project

### 6.1 Step-by-Step Execution

```bash
# 1. Clone the repository
git clone <repo-url>
cd <repo-folder>

# 2. Set up virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up credentials
copy .env.example .env
# Then edit .env with your database credentials

# 5. Run the data generation script
python scripts/script_generate_data.py

# 6. (Optional) Launch Jupyter Notebook
jupyter notebook notebooks/visulaization_retail_analysis.ipynb
```

### 6.2 Expected Output from Script
```
Connecting to PostgreSQL...
Schema and indexes created successfully.
Dimensions populated.
Generating ~70,000 sales transaction records in batches...
Batch inserted: 10000/70000 rows...
Batch inserted: 20000/70000 rows...
Batch inserted: 30000/70000 rows...
Batch inserted: 40000/70000 rows...
Batch inserted: 50000/70000 rows...
Batch inserted: 60000/70000 rows...
Batch inserted: 70000/70000 rows...

Success! 70,000 transaction rows inserted successfully into PostgreSQL.
```

---

## 7. Power BI Connection Setup

1. Open Power BI Desktop
2. Click **Get Data** → **Database** → **PostgreSQL database**
3. Enter:
   - Server: `localhost`
   - Database: `northpeak_db`
4. Select **Import** mode
5. Choose tables: `Fact_Sales`, `Dim_Date`, `Dim_Product`, `Dim_Customer`, `Dim_Geography`
6. Load and verify relationships in **Model View**

---

## 8. Troubleshooting

| Issue | Likely Cause | Fix |
|-------|-------------|-----|
| `OperationalError: could not connect` | PostgreSQL not running | Start PostgreSQL service |
| `password authentication failed` | Wrong credentials in `.env` | Check `.env` values |
| `database "northpeak_db" does not exist` | DB not created | Run `CREATE DATABASE northpeak_db;` |
| `ModuleNotFoundError: No module named 'dotenv'` | Missing packages | Run `pip install -r requirements.txt` |
| `psycopg2` install fails on Windows | Binary compatibility | Use `psycopg2-binary` (already in requirements.txt) |
| Power BI can't connect to PostgreSQL | Missing ODBC driver | Install [Npgsql driver](https://github.com/npgsql/npgsql) or use Power BI's built-in connector |
