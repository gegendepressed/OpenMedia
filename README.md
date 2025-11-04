# Introduction

OpenMedia: A Social Media WebApp that uses Flask, SQLAlchemy & Bootstrap, built with the intention to learn all these technologies hands on.

Lisence: [MIT](https://github.com/gegendepressed/OpenMedia/blob/master/LISENCE.md)

This was our B.E course's 4th semester Mini Project

# Features:
- Server side rendering using flask's jinja templating engine
- JWT like authentication using Flask login
- Reset password emails with SMTP
- Built in support for most SQL-like databases (thanks to [SQLAlchemy](https://sqlalchemy.org/))
- Cloudinary support for image hosting
- Posts, likes and per account pages support
- Moderator support (add \<Mod> in Name)
- Dark mode switch
- Mobile friendly minimalistic UI

# How to run
Run the following commands, optionally in [python venv](https://docs.python.org/3/library/venv.html) to install requirements, configure and use

1. clone the repository
```
git clone https://github.com/gegendepressed/OpenMedia.git
```
2. Install the requirements
```
pip install -r requirements.txt
```
3. Setup environment variables (these are optional, skip to step 4 if you want a basic execution )

```
# Secrets (set this to random values, used for authentication by flask)
export FLASK_SECRET_KEY=<secret_key>
export FLASK_SALT=<secret_salt>
export ITSD_SECRET_KEY=<another_secret_key>
export ITSD_SALT=<another_secret_salt>

# For cloudinary 
export CLOUDINARY_NAME=<cloudinary_name>
export CLOUDINARY_API_KEY=<cloudinary_api_key>
export CLOUDINARY_API_SECRET=<cloudinary_api_secret>

# For database 
export DATABASE_URI="database+dialect://username:password@host.url/database_name"

```

 For database you need to install [valid dialect](https://docs.sqlalchemy.org/en/20/dialects/) for the database you choose

4. Run the Application
```
python3 app.py
```
5. Production deployment

we use [gunicorn](https://gunicorn.org/) to host this application in production:
```
gunicorn -w 1 -b 0.0.0.0:80 app:app
```

# Project Structure
```
.
├── assets - Additional Assets
│   └── ...
├── instance - Prebuilt sample SQLite Database
│   └── ...
├── static - Static files that are served directly
│   └── ...
├── templates - Jinja templates for frontend
│   └── ...
├── app.py - Main Flask Code
├── fileupload.py - Cloudinary handler Code
├── form.py - Form Related helpers code
├── models.py - Database models
├── README.md
├── requirements.txt
├── temp_adddb.py - Temporary DB scripting env
└── Spacefile - hosting info (no longer used)

```
# Preview

Wan't to check out our prehosted instance? There you go: https://openmedia-e0gvb8fzbnexafd8.centralus-01.azurewebsites.net/

# Documentation

Our project report can be found here: [OpenMedia Report.pdf](https://raw.githubusercontent.com/gegendepressed/OpenMedia/refs/heads/master/assets/openmedia_report.pdf)

`bunch of AI slop though. We like writing code, not theory ;)`

# Credits
Made with ❤️ by [FrosT2k5](https://github.com/FrosT2k5), [Sairaj Pai](https://github.com/gegendepressed) & [Nandini Nichite](https://github.com/NandiniNichite)

