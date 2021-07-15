# VaccineTracker_PT
Monitor vaccine campaign in Portugal with flask in: https://vaccine-tracker-pt.herokuapp.com/

# TO DO
- add waffle graph for '% of pop vaccinates' **[DONE]**
- add new graph for proportion of vaccine types / doses
    - maybe OWID has the data + cross with dictionnary, if not: drop the idea
- figure out how to test the branch on Heroku first?  **[DONE]**
- figure out how to rebase without breaking everything...  **[DONE]**
- img Readme to update
- add footer (https://discuss.streamlit.io/t/st-footer/6447)
- add header (description of the project)
- add info under Title:
    - % of the population vaccinated
    - trend of vaccination
    - trend of infection
- add infection rate graph


## Output

<img src="http://cohenwoodworking.com/wp-content/uploads/2016/09/image-placeholder-500x500.jpg" width=400>

## How to use it locally

Create your directory clone this repo with
> git clone https://github.com/EtienneJanel/VaccineTracker_PT.git

Create virtual environment and install requirements
> python -m venv venv

> venv\\Scripts\\activate

> pip install requirements.txt

Run Streamlit application
> streamlit run app.py

## Data Source
Data source: https://github.com/owid/owid-datasets

## Blog post

More information in my blog posts:
- <a href="https://www.linkedin.com/pulse/covid19-our-next-summer-season-only-2024-etienne-janel/">Covid19 - Our next summer season? Only in 2024</a>
- <a href="https://www.linkedin.com/pulse/covid-19-ending-august-2021-etienne-janel/">Is Covid-19 ending by August 2021?</a>