# Hypothesis Testing System Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [File Structure](#file-structure)
6. [Dependencies](#dependencies)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

The Hypothesis Testing System is a web-based application designed to facilitate hypothesis testing using statistical methods. It provides a user-friendly interface for uploading datasets, selecting the type of hypothesis test, specifying the items to test, and setting the significance level (alpha).

## Features

- **Upload Data:** Users can upload datasets in CSV, Excel, or SAS7BDAT formats.
- **Select Test Type:** Users can choose between one-tailed and two-tailed hypothesis tests.
- **Specify Items:** Users can specify the items to be tested within the uploaded dataset.
- **Set Significance Level:** Users can set the significance level (alpha) for the hypothesis test.

## Installation

### Prerequisites

- Python 3.x
- Flask
- Pandas
- NumPy
- SciPy

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/Baci-Ak/Hypothesis-Testing-System.git
    ```

2. Navigate to the project directory:

    ```bash
    cd hypothesis-testing-system
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the Flask server:

    ```bash
    python app.py
    ```

2. Open your web browser and go to `http://localhost:5000`.

3. Upload your dataset and perform hypothesis tests using the web interface.

## File Structure

The project structure is as follows:

```
hypothesis-testing-system/
│
├── app.py
├── Hypothesis_testing_system.py
├── user_Interface.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── uploads/
├── templates/
│   ├── index.html
│   └── result.html
├── README.md
├── LICENSE
└── requirements.txt
```

## Dependencies

- Flask
- Pandas
- NumPy
- SciPy

## Contributing

Contributions are welcome! Please follow the guidelines outlined in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
