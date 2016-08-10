import facebook
youtoken = "EAACEdEose0cBACrLV3kVLG2whJnYwKx2D46x0FeL10aZAFAKZCoucGP7PduQp5jgteHlZBXwU5KBOb2KoZCfbJi8yYN1jDR14fCa68JcfX415dEYGK8pBt8rnhnZBaqhCX02JoXFGhwBbcCRfZAxhtjUZBXgks80kOXjxJB3OANjdzmTCCSlg5U"
graph = facebook.GraphAPI(access_token=youtoken, version='2.1')
fields_query = 'id,first_name,last_name,email,birthday,education,'
fields_query += 'gender'
event = graph.get_object(id='me', fields=fields_query)
