# QRKot service

The app for the QRKot Cat Charity Fund allows to enter information about 
donations to the foundation (without initializing the payment). Each user 
can make a donation and accompany it with a comment. Donations are not 
targeted: they are made to the fund, not to a specific project. Each donation 
received is automatically added to the first open project that has not yet 
collected the required amount. If the donation is more than the required 
amount, or if there are no open projects in the Fund, the remaining money 
is waiting for the opening of the next project. When creating a new project, 
all uninvested donations are automatically invested in the new project.

Several target projects can be opened in the QRKot Fund. Each project has 
a name, description and amount to be raised. After the required amount is 
collected, the project is closed and cannot be deleted and cannot be changed.

## Technologies

- Python 3.9;
- FastAPI;
- SQLite;
- Alembic.

## Installation and local launch
<details><summary> Instructions </summary>

- Clone the repository on local PC:

    ```bash
    git clone https://github.com/photometer/cat_charity_fund/
    ```

- Create and activate virtual environment in the project directory:

    * For Linux/MacOS
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    * For Windows
        ```bash
        python -m venv venv
        source venv/scripts/activate
        ```

- Upgrade package manager `pip` in the virtual environment and install 
necessary requirements (Windows):

    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

- Don't forget to create `.env` file and fill it up:

    ```py
    APP_TITLE=Cat charity fund QRKot
    DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
    FIRST_SUPERUSER_EMAIL=user@example.com
    FIRST_SUPERUSER_PASSWORD=string
    SECRET=<Your_secret_key>
    ```

- Launch locally:
    ```bash
    uvicorn app.main:app --reload
    ```

</details>

## API request examples

Project specification is available in `openapi.json` file in the root 
directory of the project. Download the file to view the documentation on 
[site](https://redocly.github.io/redoc/). Push `Upload a file` button at 
the top of the page and upnload the file. Project specification will be 
displayed in the ReDoc format.

## Author

[Liza Androsova](https://github.com/photometer) :sparkles:
