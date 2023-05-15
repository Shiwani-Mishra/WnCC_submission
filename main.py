import requests
import pandas as pd
from bs4 import BeautifulSoup


#fetching the website content
main_page = requests.get('https://itc.gymkhana.iitb.ac.in/wncc/soc/').text

#BeautifulSoup object to parse HTML content 
main_soup = BeautifulSoup(main_page, 'lxml')

#Extracting p elements with the class(found using Inspect)
p_elements = main_soup.find_all('p',{'class': 'lead text-center font-weight-bold text-dark'})

#Extracting the text from each p element and storing in a list:
Project_list = [p.get_text() for p in p_elements]

# Find all div elements with a given class and extract their anchor tags
project_divs = main_soup.find_all('div', class_ = 'rounded hover-wrapper pr-3 pl-3 pt-3 pb-3 bg-white')

Mentor_list=[]
Link_list=[]
Mentee_no_list=[]
for div in project_divs:
    #finding anchor tag with the link to the individual project website
    link= 'https://itc.gymkhana.iitb.ac.in/' + div.find('a', href=True)['href']
    
    Link_list.append(link)

    # Sending a GET request to project website
    response2 = requests.get(link).text
    content2 = response2

    # Creating a Beautiful Soup object for website2
    soup2 = BeautifulSoup(content2, 'lxml')

    dataset= soup2.find_all('ul')

    mentors=dataset[3].find_all('p')
    all_mentor= ''

    for mentor in mentors:
        all_mentor += mentor.text + ', '

    Mentor_list.append(mentor)
    Mentee_no_list.append(dataset[4].find('p').text)



#Creating a Pandas DataFrame with the lists
df = pd.DataFrame({'Project Name': Project_list,
                   'Mentor':Mentor_list,
                   'Number of Mentees': Mentee_no_list,
                   'Link to the project':Link_list})
print(df)
