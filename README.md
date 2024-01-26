# Netty

This is a Python Flask application built on top of an algorithm with a web scrapper logic. 
When the KNEC KCSE results are out, it takes some time for teachers to know of their students' results since the form on the KNEC site only accepts one response at a time. With Netty, you upload an excel file with the Adm Nos as well as atleast one of their names. In a split second, the results for all the students are downloaded to an excel file which is automatically downloaded on the users machine or gadget.

## Project Structure

The main files and directories in the project are as follows:

- `app.py`: This is the main Python file that runs the Flask application.
<!-- - `index.py`: This file contains the logic for handling requests and responses. -->
<!-- - `results.xlsx`: This is an Excel file that stores the results of the data processing. -->
- `static/`: This directory contains static files like CSS.
    - `css/`: This directory contains CSS files.
        - `input.css`: This is the CSS file for the input form.
        - `output.css`: This is the CSS file for the output display.
- `templates/`: This directory contains HTML templates.
    - `index.html`: This is the main HTML template for the application.
<!-- - `test.py`: This file contains unit tests for the application. -->
- `tailwind.config.js`: This is the configuration file for Tailwind CSS.
- `package.json`: This file contains the list of JavaScript dependencies for the project.
- `.vscode/`: This directory contains settings for Visual Studio Code.
- `.gitignore`: This file specifies which files and directories Git should ignore.
- `README.md`: This file provides an overview of the project and instructions for setting up, running, and testing the application.

## Setup

1. Install the required Python packages:

```bash
pip install -r requirements.txt

npm install

```

# If this brings an error like "This environment is externally managed", kindly create a virtual environment prior to the step above

## Running the Application
1. Start the Flask Server

```bash
python app.py

```

2. Open your browser and navigate to 

```
http://localhost:5000
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change

