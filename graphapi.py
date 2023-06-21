import requests

# Set your access token
access_token = ''

# Set the page ID of the public page
page_id = 'openai'

# Construct the API request URL
url = f'https://graph.facebook.com/{page_id}/posts'
params = {
    'access_token': access_token,
    'fields': 'message,created_time',  # Specify the fields you want to retrieve
    'limit': 100  # Set the number of posts to retrieve per request
}

# Send the API request
response = requests.get(url, params=params)
data = response.json()
print(data)
# Process the data
"""for post in data['data']:
    post_id = post['id']
    message = post.get('message', '')
    created_time = post.get('created_time', '')
    print(f'Post ID: {post_id}, Message: {message}, Created Time: {created_time}')"""