# Semantic Orientation Analyzer

## Project Overview
OrientX is a Python-based tool designed to classify x.com posts. Though initially developed to support a study on input-oriented and output-oriented rhetorical modes in political posts, it can serve as an analytical tool for numerous other endeavours that dammand efficient and free x.com scraping, parsing, classification, and analyses.

## Table of Contents
- Project Overview
- Features
- Installation
- Usage
- Modules
  - Web Scraper
  - Tweet Parser
  - Classifier
  - Analyzer
  - Date Parser
- License
- Acknowledgments

## Features
- Scrapes x.com posts from specified accounts.
- Parses x.com posts into data categories (e.g., likes, content, poster name, etc.).
- Classifies posts with BERT according to a trained model's domain expertise.
- Analyzes and visualizes output data (e.g., track temporal patterns of angry sentiment).
- Outputs performance metrics.

## Installation

If you already have conda setup, you can skip step 1.

1. Install Miniconda by downloading the appropriate version from [here](https://docs.anaconda.com/free/miniconda/).

   a. Choose the version that matches your processor.  
   
   b. Download the "pkg" version for easy install.


2. Open a terminal, or miniconda prompt, and clone this git repository by running:

    ```git clone https://github.com/Joseph-Hirsh/orientx```
3. Go to the AlveolEye directory

    ```cd orientx```
4. Create the conda environment

    ```conda env create -f ./environment.yml```
5. Activate the new environment

    ```conda activate orientx```
6. Install the plugin

    ```pip install .```

## Usage

Run the script by entering "orientx" in the command line along with the following options:

```plaintext
  -h, --help                     Show this help message and exit.
  --verbose                      Enable verbose output.
  --mode {run,train}             Mode of operation: "run" to scrape and classify (default), "train" to train the model.
  --accounts ACCOUNTS            JSON string for user dictionary (default: {"Labour": "https://x.com/uklabour?lang=en", "Reform":
                                  "https://x.com/reformparty_uk?lang=en"}).
  --num_posts NUM_POSTS          Number of posts to scrape per account (default: 10).
  --num_classes NUM_CLASSES      Number of classification classes (default: 3).
  --model_path MODEL_PATH        Path to the model file (default: assets/model.pth).
  --run_output_path RUN_OUTPUT_PATH
                                  Path to save classified posts CSV (default: assets/classified_posts.csv).
  --training_data TRAINING_DATA  Path to the training dataset CSV file (required for training mode).
  --num_epochs NUM_EPOCHS        Number of epochs for training (default: 10).
  --train_output_path TRAIN_OUTPUT_PATH
                                  Path to save the trained model (default: assets/model.pth).
  --max_length MAX_LENGTH        Maximum sequence length (default: 128).
  --batch_size BATCH_SIZE        Batch size for training (default: 16).
  --learning_rate LEARNING_RATE  Learning rate (default: 2e-5).
```

### Example Commands
- To **scrape and classify posts**:
  ```bash
  python main.py --mode run --num_posts 20 --run_output_path assets/classified_posts.csv
  ```
- To **train the model**:
  ```bash
  python main.py --mode train --training_data assets/training_dataset.csv --num_epochs 5 --num_classes 3
  ```

## Primary Modules

### scraper
- **Description:** Uses Playwright to log in to an x.com account and scrape posts from accounts.
- **Key Features:** Fast (considering its free) parallel scraping, error handling, x.com security evasion.

### parser
- **Description:** Parses each post, constructing a Pandas DataFrame with each row representing a post and each column representing a data category (e.g., likes, content, poster name, etc.).
- **Key Features:** Handles various tweet formats (normal, retweet, pinned) and standardizes date and number formats.

### classifier
- **Description:** Classifies tweets based on BERT domain expertise.
- **Key Features:** Fine-tunes a pre-trained BERT model with given hyperparameters, performs semantic classification with such model.

### analyzer
- **Description:** Analyzes and visualizes classified tweets.
- **Key Features:** Outputs graphs of tweet engagement over time, statistical test results.


## License
This project is licensed under the BSD 3-Clause. See the LICENSE file for details.

## Acknowledgments
- Thank you Professor Jeremy Ferwerda for letting me geek out on data science as part of my populism research!