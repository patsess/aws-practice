
import boto3

"""
Note: code is for reference only (taken from an online course)
"""


if __name__ == '__main__':
    # Generate the boto3 client for interacting with translate (for
    # translation of text into another language)
    translate = boto3.client('translate', region_name='us-east-1',
                             # Set up AWS credentials
                             aws_access_key_id=AWS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET)

    response = translate.translate_text(
        Text='Hello, how are you?',
        SourceLanguageCode='auto',  # note: should conclude English ('en')
        TargetLanguageCode='es')
    print(response['TranslatedText'])

    ######################################################################
    translated_text = translate.translate_text(
        Text='Hello, how are you?',
        SourceLanguageCode='auto',  # note: should conclude English ('en')
        TargetLanguageCode='es')['TranslatedText']

    ######################################################################
    for index, row in dumping_df.iterrows():
        # Get the public_description into a variable
        description = dumping_df.loc[index, 'public_description']
        if description != '':
            # Translate the public description
            resp = translate.translate_text(
                Text=description,
                SourceLanguageCode='auto', TargetLanguageCode='en')
            # Store original language in original_lang column
            dumping_df.loc[index, 'original_lang'] = resp['SourceLanguageCode']
            # Store the translation in the translated_desc column
            dumping_df.loc[index, 'translated_desc'] = resp['TranslatedText']

    # Preview the resulting DataFrame
    dumping_df = dumping_df[
        ['service_request_id', 'original_lang', 'translated_desc']]
    dumping_df.head()

    ######################################################################
