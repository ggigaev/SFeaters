Final Proposal
Name: SF restaurant city inspection
Description:
    1. The data includes SF city official's restaurant inspection result.
    2. Based on the inspection result, the restaurants that will fail the inspection
    within the next six months will be predicted.
    3. The primary features to be used will be the frequency and recent failures.
    Other features will be locations and types of food.
How to present the work: Presentation/slides  
Next step: Clean up the data. There are many missing coordinates of business locations.
Data source: https://data.sfgov.org/Health-and-Social-Services/Restaurant-Scores-LIVES-Standard/pyih-qa8i

1. Describe your techniques: break the data pipeline into portions and describe each one.
   1) Data collection:
       i. CSV file was downloaded.
       ii. json file was downloaded for MongoDB.
   2) Features
       i. Inspection dates: 3/2015 - 3/2018
            3/2015 - 10/2017 data will be used for training
             11/2017 - 3/2018 data will be used to label as 1 or 0
                    (1 will be violation and 0 no violation)
          More features will be created by dividing 3/2015 - 10/2017 into 6 periods, as follows,
             i) 8/2017 - 10/2017: first period
             ii) 5/2017 - 7/2017: second period
             iii) 2/2017 - 4/2017: third period
             iv) 11/2016 - 1/2017: fourth period
             v) 5/2016 - 10/2016: fifth period
             vi) 3/2015 - 4/2016: sixth period
       ii. Locations
           There are many empty cells for longitudinal/latitude information of businesses.
           Mapquest.com API will be explored to find these information.
           https://developer.mapquest.com/documentation/tools/latitude-longitude-finder/

           a). Once all the locations are filled, Kmeans will be performed to get
           the clusters with information with number of members in it.
           b). Weights will be assigned to each cluster (e.g. radius of influence),
           so that a restaurant within a cluster's radius will have higher risk
           of failure in the next inspection.

       iii. Type of food served
           There is a chance that a certain type of food they serve might have
           correlation to the frequency of violations.
           Yelp will be explored to find this information. If the information
           is found at Yelp, then Yelp information need to be joined to SF inspection
           database by business names.

      iv. Prediction
          A logistic regression will be run to predict restaurants that will
          most likely fail inspections. Public will be advised to avoid these
          restaurants for now.

2. Can you anticipate problems, what are they, do you need to overcome them now?
How do you overcome them?
    1) Missing coordinate in business locations
        There are many empty cells for longitudinal/latitude information of businesses.
        Mapquest.com API will be explored to find these information.
        https://developer.mapquest.com/documentation/tools/latitude-longitude-finder/

        At this point, I am not sure if this will work or not. Manually it is possible,
        but automatically (from programming) I am not sure. I will have to study
        how this Mapquest.com API will help me on that.

     2) Type of food served
        I will look for SF businesses from Yelp to find this information. If it is
        found, it will be still a challenge to join the name of the businesses
        from Yelp to the ones at SF city database. If Yelp data are found and the
        business names are the same as in SF city's, then it is just matter of
        setting up join between them. However, this is not SQL, so it will still
        be a challenge.
        There is no simple API for this data collection.
        Web-scraping will be done with python programming. I will have to learn
        how to do this. (Yelp allows 1000 items per request.)

3. How far do you anticipate to take the project in the allotted time frame?

    With two weeks given, I should be able to finish all the plans listed above.
    I will try as much as I can include two more features listed in item 2 above,
    but if things don't work out, then I will use zip codes for business locations.
    As for the type of food served, it may not be too much impact on the final prediction,
    from the experience.
    If time allows, it will be interesting to include the following features.
    1) Number of employees
    2) Number of years in business (year of opening)
    3) Correlation between inspection failure and Yelp ratings

4. Any other repos, libraries and other tools that you're considering using?
Are you citing them? Are you acknowledging them for their contribution?
    None at this point
    Tools I am going to use are the standard ones like Kmeans, MongoDB, requests,
    logistic regression, web-scraping.

5. Data
   csv data is located at dsi-project-proposals/sf_restaurants/data.
   "Restaurant_Scores_-_LIVES_Standard.csv"
