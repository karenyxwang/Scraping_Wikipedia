# Scraping Wikipedia

This project uses HTTP requests to receive JSON objects, and clean real HTML data from the open web. In particular, I will be scraping content from Wikipedia. The English-language Wikipedia has over 5 million articles, and about 0.1% of those have been reviewed by the community as ​Featured Articles​. The full list of all featured articles is at the following URL:

https://en.wikipedia.org/wiki/Wikipedia:Featured_articles

Wikipedia makes all public edits in the history of the wiki available through a public API, documented at 

​https://www.mediawiki.org/wiki/API:Main_page​.

1. Individual Page Scraping

    Write a function ​get_featured_biographies() ​to scrape the contents of the list of featured articles and returns a list of names for all featured articles that are also biographies. Then, answer the following questions:

- How did you determine which featured articles were biographies?

- What percentage of featured articles are biographies?

2. Scraping a dataset

    Next, write code that scrapes all of the individual pages for featured article biography titles in the list you created in part 1. Write a function ​get_first_paragraph(page)​that extracts the first paragraph of each biography.

    These functions will probably not be able to cover 100% of pages in you dataset; because the data is messy and formatted differently from page to page, they will fail on some of them. With the code you wrote, what percentage of infoboxes and first paragraphs were you able to scrape? What are the characteristics of the pages that your code fails to scrape?

3. Extracting information from messy content
    
    Using regular expressions, write a new method ​get_pronouns(text)​that determines the most common gender of pronouns in a given string of any length. Typically but not always, the three ways gender are marked in pronouns are:

- Male: he/his/him

- Female: she/her/hers

- Plural, or singular non-binary: they/them/their

    Answer the following questions abut your calculations:

- What are the drawbacks of your approach, and what types of content are excluded or missed because of the choices you made?

- What percentage of biographies use he/his pronouns, she/her, or they/them pronouns?

- What percentage of pages did your code fail to parse, or have unclear gender? Why?

4. Additional analysis

    Define and write a function that will extract one additional quantifiable feature of Wikipedia biographies based on the raw data you scraped. What question did you ask, and why is it interesting? Did you draw any new conclusions based on the feature you found and its distribution in your data? Share any statistics that support your analysis, and include those statistics in your final report.

 5. Preparing a dataset for sharing
    
    Then, either using Pandas or built-in data structures like dictionaries and lists, write a function export_dataset(df) ​that will export the values that your pronouns function calculated to a CSV or JSON file with at least three columns for each biography: the page title, the most common pronoun used in the introduction of that page, and the additional variable that you defined in part 4.

    To go along with the file, write technical documentation for how the file is constructed; your intended audience is classmates or peers that could work with you. The documentation should include:

- Explanation of the meaning of each column in your CSV file.

- Explanation of what data was not successfully scraped by your dataset-building process, and
what the limitations are on any future analyses.

- Instructions on how other data scientists could use your parsing code in their own work (you
may include Python code samples if necessary).

- Sample code that allows future users to load your file using Python and instructions on how
to run a basic analysis to confirm that they successfully downloaded the dataset.
