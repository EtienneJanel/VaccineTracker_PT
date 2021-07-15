import streamlit as st
from scripts.main import OwidData


def index():
    fig_data = OwidData()
    daily_doses = fig_data.daily_doses()
    total_doses = fig_data.total_doses()
    waffle = fig_data.waffle_plot()
    (
        remaining_pop,
        remaining_days,
        last_ma,
        total_pop,
        update_date,
    ) = fig_data.last_update()

    st.markdown(
        f"""
# Vaccine Tracker - Portugal
Hi there!  
This website aims to follow Portuguese vaccination to fight against Covid-19.

## Key metrics
_last update: {update_date}_

Portuguese population: {total_pop}  
Remaining people to vaccinate: {remaining_pop}  
Remaining days for herd immunity: {remaining_days}

"""
    )
    st.plotly_chart(waffle, use_container_width=True)

    st.markdown(
        f"""## Current Situation
From January to June the rythm of vaccination seems to follow a weekly cycle where Monday has generally the lowest injection rate, whereas the weekends have the highest.
Since July we notice missing data that we completed by linear interpolation"""
    )
    st.plotly_chart(daily_doses, use_container_width=True)

    st.markdown(
        f"""## Herd immunity
[Covid19 - Our next summer season? Only in 2024]: https://www.linkedin.com/pulse/covid19-our-next-summer-season-only-2024-etienne-janel
We are assuming most of the vaccines in portugal need 2 doses, hence herd immunity will be reached by ~12M doses
See more about how we calculated herd immunity at: [Covid19 - Our next summer season? Only in 2024]"""
    )
    st.plotly_chart(total_doses, use_container_width=True)

    st.markdown(
        f"""### Sources
[blog post: Covid19 - Our next summer season? Only in 2024]: https://www.linkedin.com/pulse/covid19-our-next-summer-season-only-2024-etienne-janel 
[blog post: Is Covid-19 ending by August 2021?]: https://www.linkedin.com/pulse/covid-19-ending-august-2021-etienne-janel/

[1]. Anderson R M, Heesterbeek H, Klinkenberg D, Hollingsworth T D. How will country-based
mitigation measures influence the course of the COVID-19 epidemic?. The Lancet. 2020 Mar;
395(10228):931-934. https://doi.org/10.1016/S0140-6736(20)30567-5

[2]. Pfizer.com. 2021. Pfizer and BioNTech Conclude Phase 3 Study of COVID-19 Vaccine Candidate,
Meeting All Primary Efficacy Endpoints | Pfizer. [online] Available at:
https://www.pfizer.com/news/press-release/press-release-detail/pfizer-and-biontech-conclude-phase-3-study-covid-19-vaccine

[3]. Salje H, Tran-Kiem C, Lefrancq N, Courtejoie N, Bosetti P, Paireau J, Andronico A, Hozé N,
Richet J, Dubost C L, Le-Strat Y, Lessler J, Levy-Bruhl D, Fontanet A, Opatowski L, Boelle P Y,
Cauchemez S. Estimating the burden of SARS-CoV-2 in France. Science. 2020 Jul. 369(6500):208-211.
https://doi.org/10.1126/science.abc3517

[blog post] Covid19 - Our next summer season? Only in 2024: https://www.linkedin.com/pulse/covid19-our-next-summer-season-only-2024-etienne-janel

[blog post] Is Covid-19 ending by August 2021?: https://www.linkedin.com/pulse/covid-19-ending-august-2021-etienne-janel/


"""
    )
