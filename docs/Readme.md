Enable 
- ### Requirements
  - #### Continuously calculate the sliding avg of the temperatures from Tweets
    - across all locations of the last n tweets.
  - ####  The number 'sliding average n' should be configurable at startup time. 
    - The input value ‘n’ should be between 2 and 100
  - #### The output of your mini-pipeline should be 2 files
    - file for the stream of temperatures in fahrenheit
    - file for the stream of the sliding averages.
  - ####  provide a high-level diagram of how you would deploy your solution




### Functional requirements
- The number of tweets to calculate the sliding average over should be configurable at startup time. 
- The input value ‘n’ should be between 2 and 100
- The output of your mini-pipeline should be 2 files, one for the stream of temperatures in fahrenheit and 1 file for the stream of the sliding averages.

### Non functional requirements
- Your solution should be
  - efficient
  - scalable
- Python is our preferred language
  - you are free to use another language
- If you are relying on any libraries or frameworks
  - please package them according to the best practices in the ecosystem.
- We will be evaluating your code for 
  - readability
  - correctness. 
- Treat this like a work submission
  - tests positive and negative
  - proper formatting
  - proper naming
  - proper documentation
  - proper error handling
  - proper logging logging
