import urllib.request
import json
import pprint as pp
import os
import argparse

def fetch_data(username):
    url = f"https://api.github.com/users/{username}/events"
    req = urllib.request.Request(url, headers={'User-Agent': 'Github-Activity-Tracker'})
    try:
        response = urllib.request.urlopen(req)
        json_string = response.read().decode('utf-8')
        data = json.loads(json_string)
        return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: Username {username} not found.")
        else:
            print(f"HTTP error {e.code}: {e.reason}.")
        return None
    except urllib.error.URLError as e:
        print(f"URL error {e.code}: {e.reason}.")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def save_to_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


def display_event_types(events):
    event_types = set()
    for event in events:
        event_types.add(event['type'])
    print(f"{event_types}\n")


def pushEventHandler(event):
    print(event['type'])
    print(f"{event['actor']['display_login']} pushed to repo {event['repo']['name']}")
    
    
def publicEventHandler(event):
    print(event['type'])
    print(f"{event['actor']['display_login']} made repo {event['repo']['name']} public")
    
    
def forkEventHandler(event):
    print(event['type'])
    print(f"{event['actor']['display_login']} forked repo {event['repo']['name']}")
    
    
def pullRequestEventHandler(event):
    print(event['type'])
    print(f'''{event['actor']['display_login']} {event['payload']['action']} a pull request for repo {event['repo']['name']}''')


def deleteEventHandler(event):
    print(event['type'])
    print(
f'''{event['actor']['display_login']} deleted a {event['payload']['ref_type']} for repo {event['repo']['name']}'''
        )
    
    
def pullRequestReviewEventHandler(event):
    print(event['type'])
    print(
f'''{event['actor']['display_login']} {event['payload']['action']} a review for pull request {event['payload']['pull_request']['number']} in repo {event['repo']['name']}'''
          )
    
    
def issueCommentEventHandler(event):
    print(event['type'])
    print(
f'''
{event['actor']['display_login']} {event['payload']['action']} comment: '{event['payload']['comment']['body']}' for issue {event['payload']['issue']['number']} for repo {event['repo']['name']}
'''
          )
    
    
def pullRequestReviewCommentHandler(event):
    print(event['type'])
    print(
f'''{event['actor']['display_login']} {event['payload']['action']} comment: '{event['payload']['comment']['body']}' for pull request {event['payload']['pull_request']['number']} for repo {event['repo']['name']}'''
    )


def createEventHandler(event):
    print(event['type'])
    if event['payload']['ref_type'] == 'repository':
        print(
f'''{event['actor']['display_login']} created a new {event['payload']['ref_type']}'''
        )
    else:
        print(
f'''{event['actor']['display_login']} created a new {event['payload']['ref_type']} in repo {event['repo']['name']}.'''
        )


def releaseEventHandler(event):
    print(event['type'])
    print(
f'''{event['actor']['display_login']} {event['payload']['action']} a release to repo {event['repo']['name']}.'''
    )
    

def issuesEventHandler(event):
    print(event['type'])
    print(
f'''{event['actor']['display_login']} {event['payload']['action']} an issue for repo {event['repo']['name']}.'''
    )


def main():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, 'data.json')
    
    parser = argparse.ArgumentParser(description="Github-User-Activity")
    parser.add_argument('username', type=str, help='Username of GitHub Account')
    
    args = parser.parse_args()
    
    event_handler = {'PushEvent': pushEventHandler,
                     'PublicEvent': publicEventHandler,
                     'ForkEvent': forkEventHandler,
                     'PullRequestEvent': pullRequestEventHandler,
                     'DeleteEvent': deleteEventHandler,
                     'PullRequestReviewEvent': pullRequestReviewEventHandler,
                     'IssueCommentEvent': issueCommentEventHandler,
                     'PullRequestReviewCommentEvent': pullRequestReviewCommentHandler,
                     'CreateEvent': createEventHandler,
                     'ReleaseEvent': releaseEventHandler,
                     'IssuesEvent': issuesEventHandler}
    
    if not args.username:
        parser.print_help()
    else:        
        events = fetch_data(str(args.username))
        
        if events is None:
            print("Could not fetch events. Exiting.")
            return

        if not events:
            print(f"No recent activity found for user '{args.username}'")
            return
    
        save_to_json(filepath, events)
        
        display_event_types(events)
        
        for event in events:
            event_handler[event['type']](event)
            print('\n')


if __name__ == "__main__":
    main()


    