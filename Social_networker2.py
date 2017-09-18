import requests, json,time
import tweepy
import networkx as nx
from networkx.readwrite import json_graph, write_gml


#set up the twitter OAuth Handler with application Token + Application Secret

auth=tweepy.OAuthHandler('','')

#set up session token using User Token and User Secret (this is mine btw)
auth.set_access_token('','')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_delay=60)

#Create Networkx graph object

G = nx.Graph()


#which users do you want to go through
users = set()

# Add the users you want to track, got lazy and haven't had a chance to write args
#users.add("")

#example data generated using these
users.add('irongeek_adc')
users.add('jaimeblascob')
users.add('josephfcox')

def main():
    try:
        requests.packages.urllib3.disable_warnings()
    except:
        pass
    
    for user in users:
        
        print "<<searching for %s's followers>>" %user
        
        G.add_node(user, color = "blue")

        try:
            # Change the API call to whatever you want to check up [in this case it's looking at friends]
            for u in tweepy.Cursor(api.friends, id = user, count = 200).items():

                fusername = u.screen_name
                        
                G.add_node(fusername, 
                        name = u.name, 
                        follower_count = u.followers_count,
                        friends = u.friends_count,
                        protected = u.protected,
                        status_count = u.statuses_count)
                        
                G.add_edge(user,fusername) 

                time.sleep(0.35)      
        
        except Exception ,e:
            print "_____something broke because of %s_______" %user
            print str(e)
        
    d = json_graph.node_link_data(G)
    json.dump(d, open('data.json', 'w'))


    # Uncomment if you want to export to .gml

    #nx.write_gml(G,"OpBeast.gml")


if __name__ == '__main__':
    main()
