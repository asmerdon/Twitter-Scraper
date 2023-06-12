import facebook as fb
import requests
access_token = ""
page_id="Prw575t187tp13"
url = f'https://graph.facebook.com/v12.0/{page_id}/posts'

params = {
    'access_token': access_token,
    'fields': 'message,created_time',  # Specify the fields you want to retrieve
    'limit': 100  # Set the number of posts to retrieve per request
}

response = requests.get(url, params=params)
data = response.json()
print(data)

"""for post in data['data']:
    post_id = post['id']
    message = post.get('message', '')
    created_time = post.get('created_time', '')
    print(f'Post ID: {post_id}, Message: {message}, Created Time: {created_time}')"""
