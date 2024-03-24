from bs4 import BeautifulSoup
import re


# Function to generate link based on exercise name
def generate_link(exercise_name):
    search_query = '+'.join(exercise_name.lower().split())
    return f"https://www.google.com/search?q={search_query}"


def get_updated_code_with_links(text):
    # Parse HTML
    soup = BeautifulSoup(text, 'html.parser')

    # Find all tables
    tables = soup.find_all('table')
    
    # Loop through each table
    for table in tables:
        # Find all rows in the table
        rows = table.find_all('tr')
        
        # Skip the header row
        for row in rows[1:]:
            # Find the exercise name (in the second column)
            exercise_cell = row.find_all('td')[1]
            exercise_name = exercise_cell.get_text(strip=True)
            
            # Generate link and replace exercise name with link
            link = generate_link(exercise_name)
            
            # Create a new anchor tag with the link
            anchor_tag = soup.new_tag('a', href=link)
            anchor_tag.string = exercise_name
            
            # Append the anchor tag after the original text
            exercise_cell.string = ''
            exercise_cell.append(anchor_tag)
            
    return soup.prettify()
