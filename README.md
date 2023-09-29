# Winter Alert System
Cloud deployed automated checking of weather conditions and recents ascents in winter climbing areas of interest.

## Objectives
- 14 day weather forcast.
- Recent ascents filted by location and grade.
- Logic to determine potential for good conditions.
- Email notification to be followed up manually.

## Stack
Serverless deployed AWS Step Function calling 4 Lambda functions in turn. The step function is triggered by a cron job or an http request (though this may be removed after testing).

- Scrape UKC for recent ascents:
    - Containerised Python Lambda required with headless Chrome driver to run Selenium.
    - Ascents data is a dynamically populated table, so a static scrape (eg. BeatifulSoup) won't suffice.
- Fetch 14 day forecast with 1 day historic conditions from MeteoBlue API.
    - Saving historic data to database to evaluate recent trends (eg. freeze-thaw conditions).
- Process Lambda with "business logic" to determine whether to send out a notification.
- Notify Lambda with a NodeJS runtime calling AWS Simple Email Service (SES).
    - `TO` and `FROM` email address as enviroment variables are maintained in the config for the notify lambda from the AWS console.