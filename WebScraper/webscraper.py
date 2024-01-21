from bs4 import BeautifulSoup as bs
import requests
import numpy as np

url_volunteer = r"https://www.volunteerconnector.org/?gclid=Cj0KCQiA-62tBhDSARIsAO7twbb_ESlqjjLnRTyiZsCdWTbXdE3KuozbMZNJVwbHGSYBOrvRlgObt2kaAg9qEALw_wcB"

def get_volunteer_opportunities():
    """
    Returns a list of dictionaries containing the title, activities, description, and dates of volunteer opportunities
    from the volunteer connector website.
    """
    response = requests.get(url_volunteer)
    soup = bs(response.text, "html.parser")
    opportunities = soup.find_all("div", class_="media")

    volunteer_opportunities = []

    for opportunity in opportunities:
        title = opportunity.find("h3", class_="title").text.strip()
        activities = opportunity.find("div", class_="activities").text.strip()
        description = opportunity.find("div", class_="description").text.strip()
        dates = opportunity.find("div", class_="dates").text.strip()

        opportunity_data = {
            "title": title,
            "activities": activities,
            "description": description,
            "dates": dates
        }

        volunteer_opportunities.append(opportunity_data)

    return volunteer_opportunities

def get_random_volunteer_opportunity():
    """
    Returns a tuple containing the title, activities, description, and dates of a random volunteer opportunity
    """
    volunteer_opportunities = get_volunteer_opportunities()
    random_opportunity = np.random.choice(volunteer_opportunities)
    return random_opportunity["title"], random_opportunity["activities"], random_opportunity["description"], random_opportunity["dates"]

print(get_random_volunteer_opportunity())