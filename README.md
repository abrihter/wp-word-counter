# wp-word-counter
Wordpress word counting script

## About
This script will allow you to count end export word count form list of WP blog articles.

You can get help on how to run the script by typing
```
python3 wp-word-count.py --help
```

### Prerequisites
To run this script you will need python3 

**Dependencies:** `lxml`.

### How to run it
To run the script you will need to have input file with list of URLs for WP blog articles you want to scan.

This is just plain text file with URL in each row.

**To run script just type:**
```
python3 wp-word-count.py -urls [URLs list file] -export [export file]
```

**Real world example:**
```
python3 wp-word-count.py -urls urls.txt -export data-export.csv
```

## Version
Current version: **1.00**

## Authors

* **Bojan** - [abrihter](https://github.com/abrihter)
