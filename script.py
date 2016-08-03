import facebook

token = 'EAANOJKNjQEABABKW251XOesurBSH4b3SAxUKCSqmC5I2fFo1Xk5ZAHNKq8SxQJiCG41t5i1uKb7te7gOBEPC0XYzCwrTbQb7NmhpI96JZBVyxmPRBmxx3fpSYOMb7gZAMCDpwjLZAZCHhPeHzim1ILuecEDDXF29gSZCmfzJXwWSJJ92KBLtBW'
token = 'DUEwPHHVcjEL5QuaNSkKvUPKNveJCbg6'
# https://graph.facebook.com/oauth/access_token?client_id=930344197111872&client_secret=845fa981312952f3dc287366e28a19d1&grant_type=client_credentials

graph = facebook.GraphAPI(token)
graph.put_object(parent_object='me',
                 connection_name='feed',
                 message='apks Hello, world')
