import requests
from bs4 import BeautifulSoup

def get_survey_numbers(district, mandal, village):
    # Send a GET request to the URL
    url = "https://dharani.telangana.gov.in/knowLandStatus"
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract available options for district, mandal, and village
    district_options = {option.text: option["value"] for option in soup.find("select", {"id": "ddldistrict"}).find_all("option")}
    mandal_options = {option.text: option["value"] for option in soup.find("select", {"id": "ddlmandal"}).find_all("option")}
    village_options = {option.text: option["value"] for option in soup.find("select", {"id": "ddlvillage"}).find_all("option")}
    
    # Check if selected district, mandal, and village are valid
    if district not in district_options:
        print("Invalid district")
        return
    if mandal not in mandal_options:
        print("Invalid mandal")
        return
    if village not in village_options:
        print("Invalid village")
        return
    
    # Send a POST request to fetch survey numbers
    data = {
        "ddlDistrict": district_options[district],
        "ddlMandal": mandal_options[mandal],
        "ddlVillage": village_options[village]
    }
    response = requests.post(url, data=data)
    
    # Parse the response and extract survey numbers
    soup = BeautifulSoup(response.content, "html.parser")
    survey_numbers = [option.text.strip() for option in soup.find("select", {"id": "ddlsurveyno"}).find_all("option")]
    
    return survey_numbers

# Example usage
district = "YourDistrict"
mandal = "YourMandal"
village = "YourVillage"

survey_numbers = get_survey_numbers(district, mandal, village)
if survey_numbers:
    print("Survey numbers for {}/{}/{}:".format(district, mandal, village))
    for survey_number in survey_numbers:
        print(survey_number)
else:
    print("Failed to retrieve survey numbers.")
