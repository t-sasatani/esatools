import os
from dotenv import load_dotenv
from piyo import Client

load_dotenv()
access_token = os.getenv('ESA_ACCESS_TOKEN')
current_team = os.getenv('ESA_TEAM_NAME')

def main():
    client = Client(
        access_token=access_token,
        current_team=current_team)
    posts = client.post(1)
    print(posts)
if __name__ == '__main__':
    main()