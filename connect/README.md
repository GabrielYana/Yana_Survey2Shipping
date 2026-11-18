# Connect Shipping

## Run the project

1. Open a terminal inside the `connect` folder.
2. Install the required packages:
   `python -m pip install -r requirements.txt`
3. Start the server:
   `python app.py`
4. Keep the terminal open and visit:
   `http://127.0.0.1:8000/`

Do not open the HTML files by double-clicking them. The pages send register and login requests to the FastAPI server, so they must be opened through the address above.

Register an account, then log in. The terminal prints the SHA-256 password hash when registration succeeds. The original `database.db` and `styles.css` are retained; the app creates a separate `users` table and does not delete the original `applicantschool` table.
