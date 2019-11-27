
import boto3

"""
Note: code is for reference only (taken from an online course)
"""


if __name__ == '__main__':
    # Generate the boto3 client for interacting with comprehend (for drawing
    # insights from text, e.g. which language it is, and its sentiment)
    comprehend = boto3.client('comprehend', region_name='us-east-1',
                              # Set up AWS credentials
                              aws_access_key_id=AWS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET)

    response = comprehend.detect_dominant_language(
        Text='Hay basura por todas partes a lo largo de la carretera.')

    print(response['Languages'][0]['LanguageCode'])
    print(response['Languages'][0]['Score'])
    # note: response['Languages'] is a list because more than one language
    # could predicted with non-trivial confidence ('Score')

    ######################################################################
    response = comprehend.detect_sentiment(
        Test='The course students are amazing.',
        LanguageCode='en')

    print(response['Sentiment'])  # e.g. 'POSITIVE'
    print(response['SentimentScore'])  # dict of confidences, e.g. 'Positive'

    ######################################################################
    # For each dataframe row
    for index, row in dumping_df.iterrows():
        # Get the public description field
        description = dumping_df.loc[index, 'public_description']
        if description != '':
            # Detect language in the field content
            resp = comprehend.detect_dominant_language(Text=description)
            # Assign the top choice language to the lang column.
            dumping_df.loc[index, 'lang'] = resp['Languages'][0][
                'LanguageCode']

    # Count the total number of spanish posts
    spanish_post_ct = len(dumping_df[dumping_df.lang == 'es'])

    # Print the result
    print("{} posts in Spanish".format(spanish_post_ct))

    ######################################################################
    for index, row in dumping_df.iterrows():
        # Get the translated_desc into a variable
        description = dumping_df.loc[index, 'public_description']
        if description != '':
            # Get the detect_sentiment response
            response = comprehend.detect_sentiment(
                Text=description,
                LanguageCode='en')
            # Get the sentiment key value into sentiment column
            dumping_df.loc[index, 'sentiment'] = response['Sentiment']

    # Preview the dataframe
    dumping_df.head()

    ######################################################################
    for index, row in scooter_requests.iterrows():
        # For every DataFrame row
        desc = scooter_requests.loc[index, 'public_description']
        if desc != '':
            # Detect the dominant language
            resp = comprehend.detect_dominant_language(Text=desc)
            lang_code = resp['Languages'][0]['LanguageCode']
            scooter_requests.loc[index, 'lang'] = lang_code
            # Use the detected language to determine sentiment
            scooter_requests.loc[index, 'sentiment'] = \
            comprehend.detect_sentiment(
                Text=desc,
                LanguageCode=lang_code)['Sentiment']

    # Perform a count of sentiment by group.
    counts = scooter_requests.groupby(['sentiment', 'lang']).count()
    counts.head()

    ######################################################################
