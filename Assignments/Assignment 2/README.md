# Assignment 2: Bitly Clone

### Problem Statement
Create a Bitly clone using Flask.

## Run Project:
- Run below commands from ***assignment_root*** directory for starting server.

  * **Run Server**: This will start flask server which will host various APIs to create,shorten,retrieve,update long urls.
    ```
    flask run
    ```
    
  * **Create Bitlink**: This will create bitlink
      ```
      curl --location --request POST 'http://127.0.0.1:5000/create' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "long_url": "https://www.programiz.com/python3-programming/datetime",
        "title": "HT API Documentation",
        "domain": "http://localhost:5000",
        "tags": [
          "ht",
          "api"
        ]
    }'
      ```
    
  * **Retrieve Bitlink**: This will retrieve url
      ```
      curl --location --request GET 'http://127.0.0.1:5000/bitlinks/http://localhost:5000/15FTGi'
      ```
 
  * **Shorten Bitlink**: This will Shorten url
      ```
      curl --location --request POST 'http://127.0.0.1:5000/shorten' \
      --header 'Content-Type: application/json' \
      --data-raw '{
        "long_url": "https://www.programiz.com/python3-programming/datetime",
        "domain": "http://localhost:5000"
      }'
      ```
     
  * **Update Bitlink**: This will update bitlink
      ```
      curl --location --request PATCH 'http://127.0.0.1:5000/bitlinks/http://localhost:5000/15FTGi' \
      --header 'Content-Type: application/json' \
      --data-raw '{
        "long_url": "https://www.programiz.com/python3-programming/",
        "title": "API Documentation python3",
        "tags": [
          "python3",
          "api"
         ]
       }'
      ```
  * **Hit Bitlink**: This will hit bitlink which has domain as localhost:5000
    ```
    curl --location --request GET 'http://localhost:5000/15FTGi'
    ```
  
  * **Clicks**: This will get number of clicks for given bitlink
     ```
     curl --location --request GET 'http://127.0.0.1:5000/bitlinks/http://localhost:5000/15FTGi/clicks'
     ```
 