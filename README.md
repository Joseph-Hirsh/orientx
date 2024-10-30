# OrientX

*Note: This project is nascent. It lacks sufficient printing/logging, error handling, documentation, unit tests, and config files for constants. One can also imagine numerous feature and user-experience updates.*

## Project Overview
OrientX is a Python-based tool designed to classify x.com posts. Though initially developed to support a study on input-oriented and output-oriented rhetorical modes in populist social media posts, it can serve as an analytical tool for numerous other purposes that demand efficient and free x.com scraping, parsing, classification, and analyses.

## Table of Contents
- Project Overview
- Features
- Installation
- Usage
- Module descriptions
- License
- Acknowledgments

## Features
- Scrapes x.com posts from specified accounts.
- Parses x.com posts into data categories (e.g., likes, content, poster name, etc.).
- Classifies posts with BERT according to a trained model's domain expertise.
- Analyzes and visualizes output data (e.g., track temporal patterns of angry sentiment).
- Outputs performance metrics.

## Installation



1. (Skip if you have conda) - Install Miniconda by downloading the appropriate version from [here](https://docs.anaconda.com/free/miniconda/):

   a. Choose the version that matches your processor.  
   
   b. Download the "pkg" version for easy install.


2. Open a terminal, or miniconda prompt, and clone this git repository by running:

    ```git clone https://github.com/Joseph-Hirsh/orientx```
3. Go to the orientx directory:

    ```cd orientx```
4. Create the conda environment:

    ```conda env create -f ./environment.yml```
5. Activate the new environment:

    ```conda activate orientx```
6. Install the plugin:

    ```pip install .```
7. Add X account credentials to `assets/credentials.ini` (use accounts that you would not mind getting banned!). The credentials file contains a template, so adding accounts should be straightforward. 


## Usage

### Run everything at once:

Run the entire scraper > parser > classifier > analyzer pipeline using this command:

```plaintext
  usage: orientx [-h] [--accounts ACCOUNTS] [--num_posts NUM_POSTS] [--scrape_batch_size SCRAPE_BATCH_SIZE] [--scroll_mode {manual,auto}] [--mode {inference,train}]
               [--num_classes NUM_CLASSES] [--model_path MODEL_PATH] [--learning_rate LEARNING_RATE] [--max_input_length MAX_INPUT_LENGTH] [--test_size TEST_SIZE]
               [--train_batch_size TRAIN_BATCH_SIZE] [--num_epochs NUM_EPOCHS] [--train_output_path TRAIN_OUTPUT_PATH] [--training_data TRAINING_DATA] [--output_path OUTPUT_PATH]
               [--quiet]
```

### Recommended: Run each module at a time 

Note: This will save the results of each, allowing you to rerun parts of the pipeline with different parameters.

Run the scraper:

```plaintext
  usage: orientx-scrape [-h] [--accounts ACCOUNTS] [--num_posts NUM_POSTS] [--scrape_batch_size SCRAPE_BATCH_SIZE] [--scroll_mode {manual,auto}] [--output_path OUTPUT_PATH]
                      [--quiet]
```

Run the parser (use the output path of a scrape job as the input path):

```plaintext
  usage: orientx-parse [-h] [--input_path INPUT_PATH] [--output_path OUTPUT_PATH] [--quiet]
```

Run the classifier (use the output path of a parse job as the input path):

```plaintext
  usage: orientx-classify [-h] [--mode {inference,train}] [--num_classes NUM_CLASSES] [--model_path MODEL_PATH] [--learning_rate LEARNING_RATE]
                        [--max_input_length MAX_INPUT_LENGTH] [--test_size TEST_SIZE] [--train_batch_size TRAIN_BATCH_SIZE] [--num_epochs NUM_EPOCHS]
                        [--train_output_path TRAIN_OUTPUT_PATH] [--training_data TRAINING_DATA] [--input_path INPUT_PATH] [--quiet]
```

Run the analyzer (use the output path of a classifier job as the input path):

```plaintext
  usage: orientx-analyze [-h] [--input_path INPUT_PATH] [--quiet]
```

### Example
```plaintext
  coming soon
```

## Primary Modules

### scraper
- **Description:** uses Playwright to log in to an x.com account and scrape posts from accounts.
- **Key Features:** fast (considering its free) parallel scraping, error handling, and x.com security evasion.

### parser
- **Description:** parses each post, constructing a Pandas DataFrame with each row representing a post and each column representing a data category (e.g., likes, content, poster name, etc.).
- **Key Features:** handles various tweet formats (normal, retweet, pinned) and standardizes date and number formats.

### classifier
- **Description:** classifies tweets based on BERT domain expertise.
- **Key Features:** fine-tunes a pre-trained BERT model with given hyperparameters, performs semantic classification with such model.

### analyzer
- **Description:** analyzes and visualizes classified tweets.
- **Key Features:** outputs graphs of tweet engagement over time, statistical test results.


## License
This project is licensed under the BSD 3-Clause. See the LICENSE file for details.

## Acknowledgments
- Thank you Professor Jeremy Ferwerda for letting me geek out on data science as part of my populism research!