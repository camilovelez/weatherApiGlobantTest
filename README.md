This application retrieves current and forecasted weather data from a selected city in the world

To start the application first install the required libraries running `pip install -r requirements.txt` at root level and then perform either of the following:
- Set the enviroment variable FLASK_APP to `FLASK_APP=app.py` and run `flask run`
- Run `python app.py` at root level

The app consists of an endpoint which must be called as: 
<pre><code>GET /weather?city=$City&country=$Country  </code></pre>
with $Country being a 2 letter country id

To execute the unit tests start the application and run `python tests.py` at root level

Notes: 
- The console prints that start with "Exception thrown while" when executing the unit tests are prints that I myself added to certain functions
- Rather than validating if $Country is all in lower case, I decided setting it to lower case in the endpoint

Possible improvements which I didn't have time to implement:
- Using a distributed cache such as redis rather than the local storage to cache the data
- Perform the two requests to the external api's endpoints in parallel
- Having more detailed error messages when either the requests fail or the data don't match the expected format
- Add unit tests for the caching functionality. I manually tested it using prints and it works