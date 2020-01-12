import re
import pandas as pd
from pandas.io.json import json_normalize
from wiki_api import page_text
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt


# This function first scrapes the contents of page Wikipedia:Featured_articles.
# This function then documents the list of names of all featured articles in featured_articles_names.
# This function then documents the list of names of all featured articles that are also biographies in biographies_names.
# This function finally returns the names of biographies featured articles.
def get_featured_biographies():
    page = page_text('Wikipedia:Featured_articles', 'html')
    soup = BeautifulSoup(page, 'html.parser')
    featured_articles_names = []
    for sub in soup.find('h2').parent.descendants:
        if sub.name == 'li':
            featured_articles_names.append(sub.string)
    biographies_names = []
    for h3 in soup.find_all('h3'):
        for sub in h3.children:
            if('mw-headline' in sub.get('class', '') and 'biographies' in sub.string):
                for li in h3.next_sibling.next_sibling.children:
                    if li.name == 'li':
                        biographies_names.append(li.string)
                break
    return biographies_names

# This function calculates the percentage of featured articles that are biographies. 
def Wiki_Q1():
    page = page_text('Wikipedia:Featured_articles', 'html')
    soup = BeautifulSoup(page, 'html.parser')
    featured_articles_names = []
    for sub in soup.find('h2').parent.descendants:
        if sub.name == 'li':
            featured_articles_names.append(sub.string)
    biographies_names = get_featured_biographies()
    percentage_of_biographies = len(biographies_names)/len(featured_articles_names) * 100
    print(f"Total articles: {len(featured_articles_names)}")
    print(f"Biographies articles: {len(biographies_names)}")
    print(f"Percentage of biographies: {percentage_of_biographies:.2f}%")


# This function takes the titles of pages as input.
# This function finds the p tag of the first empty class for the page and scrapes the paragraph.
def get_first_paragraph(page):
    first_paragraphs = ''
    try:
        soup = BeautifulSoup(page_text(page, 'html'), 'html.parser')
        for p in soup.find_all('p'):
            if(p.get('class', '') == ''):
                for paragraph in p.children:
                    first_paragraphs += str(paragraph.string)
                break
    except Exception as e:
        pass
    return first_paragraphs
 
# This function first extracts the first paragraph for each biography.
# This function then writes the first paragraphs in file first_paragraphs.txt.
# This function finally calculates the percentage of pages that were scraped.
def Wiki_Q2():
    biographies_names = get_featured_biographies()
    number_of_failures = 0
    with open('first_paragraphs.txt', 'w') as f:
        for name in biographies_names:
            try:
                first_paragraph = get_first_paragraph(name)
                paragraph = name+'\n'+str(first_paragraph)+'\n\n'
            except Exception as e:
                number_of_failures += 1
                pass
            f.write(paragraph)
    percentage_of_success = 100 - number_of_failures/len(biographies_names) * 100
    print(f'{percentage_of_success:.2f}% of first paragraphs were scraped.')
    print('The first paragraph of each biography has been written in file first_paragraphs.txt')


# This function takes text as input.
# This function calculates the number of each pronouns and return the maximum of them.
def get_pronouns(text):
    gender = ['Male', 'Female', 'Plural']
    count = [0, 0, 0]
    count[0] = len(re.findall(' he ', text))+len(re.findall(' his ', text))+len(re.findall(' him ', text))
    count[1] = len(re.findall(' she ', text))+len(re.findall(' her ', text))
    count[2] = len(re.findall(' they ', text))+len(re.findall(' them ', text))+len(re.findall(' their ', text))
    return gender[count.index(max(count))]

# This function first extracts the maximum pronoun of each page.
# This function then counts the number of each pronoun from all biographies.
# This funtion finally calculates the percentage of each pronoun in biographies. 
def Wiki_Q3():
    biographies_names = get_featured_biographies()
    number_of_failures = 0
    num_male, num_female, num_plural, num_unknown = 0, 0, 0, 0
    for name in biographies_names:
        try:
            text = page_text(name, 'text')
            gender = get_pronouns(text)
            if(gender == 'Male'):
                num_male += 1
            elif(gender == 'Female'):
                num_female += 1
            elif(gender == 'Plural'):
                num_plural += 1
            else:
                num_unknow += 1
        except Exception as e:
            number_of_failures += 1
            pass
    percentage_of_male = num_male/len(biographies_names) * 100
    percentage_of_female = num_female/len(biographies_names) * 100
    percentage_of_plural = num_plural/len(biographies_names) * 100
    percentage_of_unknown = num_unknown/len(biographies_names) * 100
    percentage_of_failures = number_of_failures/len(biographies_names) *100
    print(f'{percentage_of_male:.2f}% biographies use he/his pronouns.')
    print(f'{percentage_of_female:.2f}% biographies use she/her pronouns.')
    print(f'{percentage_of_plural:.2f}% biographies use they/them pronouns.')
    print(f'{percentage_of_unknown:.2f}% biographies use unknown pronouns.')
    print(f'Failed to parse {percentage_of_failures:.2f}% of pages.')


# This function first calculates the number of words of each biography.
# This function then calculates the maximum, minimum, mean, median and standard deviation of the word counts of all biographies. 
def additional_analysis():
    biographies_names = get_featured_biographies()
    page_length = []
    for name in biographies_names:
        try:
            biography_text = page_text(name,'text')
            length = len(biography_text.split())
            page_length.append(length)
        except:
            pass
    max_length = max(page_length)
    min_length = min(page_length)
    mean_length = np.mean(page_length)
    median_length = np.median(page_length)
    std_length = np.std(page_length)
    print(f'max: {max_length}, min: {min_length}, mean: {mean_length:.2f}, median: {median_length}, std: {std_length:.2f}')


# This function exports csv file.
def export_dataset(df):
    df.to_csv('export_dataset.csv', index=False)
    print('Data frame is saved in export_dataset.csv')

# This function first extracts the titles of biographies.
# This function then extracts the pronoun and length of each biography and adds them to a list.
# This function then saves the results to file export_dataset.csv
def Wiki_Q5():
    biographies_names = get_featured_biographies()
    list_biography = []
    number_of_failures = 0
    for name in biographies_names:
        try:
            biography_text = page_text(name, 'text')
            gender = get_pronouns(biography_text)
            length = len(biography_text.split())
            list_biography.append({'title': name, 'pronoun': gender, 'len': length})
        except Exception as e:
            number_of_failures += 1
            pass
    print(f'Failed to scrape {number_of_failures} pages.')
    df_biography = pd.DataFrame(list_biography, columns=['title', 'pronoun', 'len'])
    export_dataset(df_biography)
    print(pd.read_csv('export_dataset.csv'))


# This function first sets (born, dead) as (-1, -1) for missing data.
# This function then finds out the date of birth and death in the infobox.
# This function finally returns the date of birth and death.
def get_birth_and_death(infobox):
    born, dead = -1, -1
    for tbody in infobox.children:
        for tr in tbody.children:
            pattern = "\d{4}"
            if('Born' in tr.contents[0]):
                born = int(re.findall(pattern, str(tr))[0])
            elif('Died' in tr.contents[0]):
                dead = int(re.findall(pattern, str(tr))[0])
    return (born, dead)


# This function first examines if there is infobox in the page.
# For the page that has infobox, this function then retrieves the date of birth and death.
# This function then calculates the number of biography that has birth date but no death date.
# This function also calculates the number of biography that has unknown date.
# This function finally calculates the percentage. 
def Extra_Credit():
    biographies_names = get_featured_biographies()
    num_no_infobox = 0
    birth_and_death = []
    year_list = []
    for name in biographies_names:
        try:
            page = page_text(name, 'html', include_tables=True)
            soup = BeautifulSoup(page, 'html.parser')
            if('infobox biography vcard' in page):
                table = soup.find_all('table', 'infobox biography vcard')[0]
                year = (get_birth_and_death(table))
                year_list.append(year)
            else:
                year = (-1, -1)
                num_no_infobox += 1
                year_list.append(year)
        except Exception as e:
            year = (-1, -1)
            year_list.append(year)
        years_dictionary = {
            'title': name,
            'year': year
        }
        birth_and_death.append(years_dictionary)
    df = pd.DataFrame(birth_and_death)
    df.to_csv('extra_credit.csv', index=False)
    print('Extra credit is saved in extra_credit.csv')
    plt.boxplot(year_list[0])
    plt.boxplot(year_list[1])
    plt.show()

    born, died = [], []
    no_birth, no_death, unknown = 0, 0, 0
    for i in year_list:
        if(i[0] == -1 and i[1] == -1):
            unknown += 1
        elif(i[0] == -1 and i[1] != -1):
            no_birth += 1
            died.append(i[1])
        elif(i[0] != -1 and i[1] == -1):
            born.append(i[0])
            no_death += 1
        else:
            born.append(i[0])
            died.append(i[1])
    percentage_of_alive = no_death/len(year_list) * 100
    percentage_of_unknown = unknown/len(year_list) * 100
    print(f'{percentage_of_alive:.2f}% people are still alive.')
    print(f'{percentage_of_unknown:.2f}% featured biographies are unknown.')



if __name__ == "__main__":

    Wiki_Q1()
    Wiki_Q2()
    Wiki_Q3()
    additional_analysis()
    Wiki_Q5()
    Extra_Credit()
    


