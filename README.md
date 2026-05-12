# ✝️ ChristianBlue Business Directory Scraper

A two-stage Python scraper for **[ChristianBlue.com](https://christianblue.com)** — a Christian business directory. It first collects all category URLs, then extracts full business profiles including contact details, social media links, descriptions, logos, and more — saved to a CSV file with automatic pagination support.

---

## 📁 Project Structure

```
christianblue-scraper/
│
├── links.py          # Stage 1: Collect category URLs from the directory
├── cristion.py       # Stage 2: Scrape business profiles from each category page
│
├── links.csv         # Stage 1 output — category URLs (auto-generated)
└── BlueCristion.csv  # Stage 2 output — full business profiles (auto-generated)
```

---

## ✨ Features

- **Two-stage pipeline**: Cleanly separates link collection from data extraction.
- **BeautifulSoup + Selenium hybrid**: Uses Selenium for browser control and pagination, BeautifulSoup for fast HTML parsing of listing cards.
- **Auto pagination**: Detects and clicks the "Next page" button automatically until all pages are exhausted.
- **Ad/popup dismissal**: Automatically closes any popup ads on page load.
- **Rich business data**: Extracts 15 fields per listing including phone, address, Google Maps direction link, email, website, social media, logo, description, and advertiser year.
- **Anti-detection**: Disables `AutomationControlled` Chrome flag to reduce bot detection.
- **Auto ChromeDriver management**: Uses `webdriver_manager` — no manual driver downloads needed.

---

## 🔧 Requirements

### Python Version
- Python 3.8+

### Dependencies

```bash
pip install selenium webdriver-manager beautifulsoup4 pandas
```

| Package              | Purpose                                          |
|----------------------|--------------------------------------------------|
| `selenium`           | Browser automation and pagination                |
| `webdriver-manager`  | Auto-installs matching ChromeDriver              |
| `beautifulsoup4`     | Fast HTML parsing of listing cards               |
| `pandas`             | CSV output management                            |

---

## 🚀 Getting Started

### Step 1 — Collect Category URLs

Run `links.py` to scrape all category links from the ChristianBlue categories page:

```bash
python links.py
```

This generates `links.csv` with three columns:

| Field          | Description                          |
|----------------|--------------------------------------|
| `Category`     | Category name (e.g., "Accountants")  |
| `Sub Category` | Sub-category name (empty by default) |
| `URL`          | Full category page URL               |

---

### Step 2 — Scrape Business Profiles

Run `cristion.py` to read `links.csv` and extract all business listings:

```bash
python cristion.py
```

The script reads each URL from `links.csv`, scrapes all listing cards across all pages, and appends results to `BlueCristion.csv`.

---

## 📊 Output Data Format

### Stage 1 — `links.csv`

| Field          | Description                    |
|----------------|--------------------------------|
| `Category`     | Business category name         |
| `Sub Category` | Sub-category (if applicable)   |
| `URL`          | ChristianBlue category page URL|

### Stage 2 — `BlueCristion.csv`

| Field                 | Description                                        |
|-----------------------|----------------------------------------------------|
| `Category`            | Business category                                  |
| `Sub Category`        | Sub-category                                       |
| `Title`               | Business name                                      |
| `Phone`               | Phone number (stripped of `tel:`)                  |
| `Address`             | Street address                                     |
| `Direction`           | Google Maps direction link                         |
| `Year Advertiser`     | Year the business started advertising              |
| `Company Description` | Business description text                          |
| `Website`             | Official website URL                               |
| `Email`               | Email address (stripped of `mailto:`)              |
| `Facebook`            | Facebook page URL                                  |
| `LinkedIn`            | LinkedIn profile URL                               |
| `Instagram`           | Instagram profile URL                              |
| `Twitter`             | Twitter/X profile URL                              |
| `Logo`                | Business logo image URL                            |

---

## 🏗️ Architecture Overview

```
links.py
    └── CristianBlueLinks                  # Link collector
        ├── __init__()                     # Launch Chrome with anti-detection flag
        ├── land_targeted_page()           # Navigate to categories page
        └── get_all_links()               # Extract all category h2 links → links.csv

cristion.py
    └── CristianBlueScraper               # Business profile scraper
        ├── __init__()                    # Launch Chrome, init Selenium + BeautifulSoup
        ├── extract_element()             # CSS selector extraction (text or attribute)
        ├── extract_element_by_text()     # Find element by its visible text content
        ├── land_targeted_page()          # Navigate to URL, dismiss popups
        ├── handle_pagination()           # Click "Next page" button
        └── get_all_data()               # Parse all cards on page → append to CSV

    └── Main loop
        ├── Reads links.csv row by row
        ├── Navigates to each category URL
        └── Paginates until no more pages → moves to next category
```

---

## ⚙️ Configuration

### Changing the Target Site or Start URL

In `links.py`:
```python
bot.land_targeted_page('https://christianblue.com/categories/')
```

### Changing the Output Filename

In `cristion.py`:
```python
p.to_csv("BlueCristion.csv", ...)  # Change filename here
```

### Skipping Already-Scraped Categories

Manually remove rows from `links.csv` before running `cristion.py` to skip categories you've already processed.

---

## ⚠️ Notes & Limitations

- **Single-threaded**: Unlike other scrapers in this series, ChristianBlue runs sequentially (no multi-threading) to avoid rate limiting on a smaller directory site.
- **Implicit waits** are used alongside `time.sleep()` — adjust values if the site is slow to load.
- The scraper uses `BeautifulSoup` on the page source rather than live Selenium element queries for faster card parsing.
- If `links.csv` already exists from a previous run, new rows will be appended. Delete it before a fresh run to avoid duplicates.
- Scraping ChristianBlue.com may be subject to their [Terms of Service](https://christianblue.com). Use responsibly.

---

## 📌 Example Usage

```python
# Run only a specific category manually
bot = CristianBlueScraper()
bot.land_targeted_page("https://christianblue.com/category/accountants/")
while True:
    try:
        bot.get_all_data(cat="Accountants", sub_cat="")
        bot.handle_pagination()
    except:
        break
```

---

## 🏷️ Repo Name & Description

**Repo name:** `christianblue-directory-scraper`

**Description:** `Two-stage Python scraper for ChristianBlue.com — collects category URLs then extracts 15 business profile fields including contacts, social links, and logos using Selenium and BeautifulSoup with auto-pagination.`

---

## 👤 Author

**Muhammad Anwaar Rasool**
Automation & Web Scraping Engineer

---

## 📄 License

This project is for educational and personal use only. The author is not responsible for any misuse of this tool.
