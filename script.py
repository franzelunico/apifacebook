import facebook
token = 'EAACEdEose0cBAMgC8RadjR9eW9Hu3soNo7emA8vgToZAZAmmYa2nWeJhBpeyfhZASvsgF5NvZBGJfxVZA3AWV5CFSZCpjZA845DaVPWNqZCP3MVEgPdqOODjsCGYhvsjcTxBLje1m29cW5NZCwYbueSeP4mKp0kj4HtxLIOYCQZA8ZBfwTkODXe5Gt8'
# graph = facebook.GraphAPI(token)
# graph.put_object(parent_object='me',
#                  connection_name='feed',
#                  message='apks Hello, world')

graph = facebook.GraphAPI(token)
# me/friends/
friends = graph.get_connections(id='me', connection_name='friends')
info ='id,name,picture,first_name,email'
event = graph.get_object(id='me', fields=info)
# https://graph.facebook.com/v2.0/me/friends
# https://graph.facebook.com/v2.0/me/friends?access_token=EAACEdEose0cBAKVjZBWPNfawhZCPUeMwdQEDZAJ8ZBnq0jaw02h373bigkZBDaOFm9kgt8b9E3lVl1kdZAfZCyGwlBdeVXW0nDi7KzBtylQuR1gY0Scmjp3651dJeP5wnlNpZCvqZApYb6C15Nmrpoz6gK9IKnxZCtoDedBw9G2nc88TiO1bi7rZBbr

