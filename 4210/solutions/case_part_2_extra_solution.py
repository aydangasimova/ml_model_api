"""
Case: Model Operationalization
Part 2 extra: Calling your own API from python and callign public APIs

Good luck and have fun!
---------------------------

In this extra part you will first call your own API from python.
Next, we will call some public APIs from python!

Follow along with the exercises below. Tip: It can be helpful to run (parts of) the code in Jupyter
Notebook to test them.

"""

from flask import Flask, request, send_file


# Extra Exercise 1: Calling your API

""""
In this script we will call our API directly from python.
This is similar to how you will call external APIs that you are not hosting on your own sever.
Pick a route from your server in exercise 2 and call it from within Python!
"""

#Fill in the gaps below:

# The API endpoint
endpoint = 'http://127.0.0.1:5008/predict_post'


# The request parameters (in a Python dictionary)
data = {'average_montly_hours':300,'number_project':3
          ,'last_evaluation':0.2,'satisfaction_level':0.2
          ,'salary':'low','department':'other' }

# Make the request
r = requests.post(url = endpoint, data = data)

# Extract the response
response_text = r.text
print(response_text)

# Output should be "Prediction: Employee will leave"

# Extra Exercise 2: Calling your first external API

"""
You just called your own API from within Python, great job!
We can call public APIs in exactly the same way.
In this exercise you free to pick one of the APIs below. Pick the one that excites you the most!

For the API call, be sure to retrieve the part of the response that is relevant to show.
So only select the joke or life advice from the response the API provides.

- Joke API. This API returns a dad joke, for whenever you need a laugh.
Documentation: https://icanhazdadjoke.com/api
Be sure to pass the "Accept": "text/plain" header when making the request. (do you know why?)

- Life advice API. This API returns some life advice to you. We can all use this!
Documentation: https://api.adviceslip.com/
Go for the random advice part
Be sure to pass the "Accept": "text/plain" header when making the request.
"""

# Call the API of your choice. Select the relevent part of the response and print that.
# Dad jokes
data = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "text/plain"}).text

# Life advice
data = requests.get('https://api.adviceslip.com/advice', headers={"Accept": "text/plain"}).json()['slip']['advice']

print(data)


# Extra Exercise 3: Calling a public API from your API

""""
Congratulations for making it to this part champion! Now it's time to call a public API from our own
API and do something with the response from the public API.

We will use a public API to receive the URL to a random dog picture. But showing just the URL is not
that exciting. So you will use your own API to call the public API, receive the URL and then return
the image to the browser (like with the GIFs).

- Hint: this will not work with send_file that you used before, because send_file is used for local
  files. Instead, you can send some HTML with the link in it for example.

- Dog picture API. This API provides you with the URL to a dog picture, now that's instant
  happiness.
Main page: https://random.dog/
API route: https://random.dog/woof.json
Extra assignment if you pick the dog picture: create an API route on your flask app from exercise 2
that call the dog API. Return the picture to the browser and show it (like you did with the gifs).
"""


# Code here

# Dog picture
text = requests.get('https://random.dog/woof.json').json()
data = text['url']


# Extra Exercise 4: Calling a more complex public API
""""
For the final exercise you can call any API you want!
Be aware that APIs like Spotify's require some complex authorization setup.
You just have to do that once, but it might take too long for now.

You can pick one of the APIs you found in the exercise from this morning.
Or if you need some extra inspiration: https://blog.snap.hr/24/09/2018/25-crazy-apis-next-project/
"""

# Code here
