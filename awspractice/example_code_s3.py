
import boto3
import pandas as pd

"""
Note: code is for reference only (taken from an online course)
"""


if __name__ == '__main__':
    # Generate the boto3 client for interacting with S3 (for data storage)
    s3 = boto3.client('s3', region_name='us-east-1',
                      # Set up AWS credentials
                      aws_access_key_id=AWS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET)

    # Create the buckets
    response_staging = s3.create_bucket(  # e.g. for raw input
        Bucket='pat-aws-practise-staging')
    response_processed = s3.create_bucket(  # e.g. for processed data
        Bucket='pat-aws-practise-processed')

    # # Delete the gim-test bucket
    # s3.delete_bucket(Bucket='pat-aws-practise-test')

    # Print out the response
    print(response_staging)

    # List the buckets
    buckets = s3.list_buckets()

    # Print the buckets
    print(buckets)

    # Iterate over Buckets from .list_buckets() response
    for bucket in response_staging['Buckets']:
        # Print the Name for each bucket
        print(bucket['Name'])

    ######################################################################
    # Upload final_report.csv to pat-aws-practice-staging
    s3.upload_file(Bucket='pat-aws-practise-staging',
                   # Set filename and key
                   Filename='final_report.csv',
                   Key='2019/final_report_01_01.csv')

    # Get object metadata and print it
    response = s3.head_object(Bucket='pat-aws-practise-staging',
                              Key='2019/final_report_01_01.csv')

    # Print the size of the uploaded object
    print(response['ContentLength'])

    ######################################################################
    # List only objects that start with '2018/final_'
    response = s3.list_objects(Bucket='pat-aws-practice-staging',
                               Prefix='2018/final_')

    # Iterate over the objects
    if 'Contents' in response:
        for obj in response['Contents']:
            # Delete the object
            s3.delete_object(Bucket='pat-aws-practice-staging', Key=obj['Key'])

    # Print the keys of remaining objects in the bucket
    response = s3.list_objects(Bucket='pat-aws-practice-staging')

    for obj in response['Contents']:
        print(obj['Key'])

    ######################################################################
    # Upload the final_report.csv to pat-aws-practice-staging bucket
    s3.upload_file(
        # Complete the filename
        Filename='./final_report.csv',
        # Set the key and bucket
        Key='2019/final_report_2019_02_20.csv',
        Bucket='pat-aws-practice-staging',
        # During upload, set ACL to public-read
        ExtraArgs={
            'ACL': 'public-read'})

    ######################################################################
    # List only objects that start with '2019/final_'
    response = s3.list_objects(
        Bucket='pat-aws-practice-staging', Prefix='2019/final_')

    # Iterate over the objects
    for obj in response['Contents']:
        # Give each object ACL of public-read
        s3.put_object_acl(Bucket='pat-aws-practice-staging',
                          Key=obj['Key'],
                          ACL='public-read')

        # Print the Public Object URL for each object
        print("https://{}.s3.amazonaws.com/{}"
              .format('pat-aws-practice-staging', obj['Key']))

    ######################################################################
    # Generate presigned_url for the uploaded object
    share_url = s3.generate_presigned_url(
        # Specify allowable operations
        ClientMethod='get_object',
        # Set the expiration time
        ExpiresIn=3600,  # note: one hour
        # Set bucket and shareable object's name
        Params={'Bucket': 'pat-aws-practice-staging',
                'Key': 'final_report.csv'}
    )

    # Print out the presigned URL
    print(share_url)

    ######################################################################
    df_list = []

    for file in response['Contents']:
        # For each file in response load the object from S3
        obj = s3.get_object(Bucket='pat-aws-practice-requests',
                            Key=file['Key'])
        # Load the object's StreamingBody with pandas
        obj_df = pd.read_csv(obj['Body'])
        # Append the resulting DataFrame to list
        df_list.append(obj_df)

    # Concat all the DataFrames with pandas
    df = pd.concat(df_list)

    # Preview the resulting DataFrame
    df.head()

    ######################################################################
    # Generate an HTML table with no border and selected columns
    services_df.to_html('./services_no_border.html',
                        # Keep specific columns only
                        columns=['service_name', 'link'],
                        # Set border
                        border=0)

    # Generate an html table with border and all columns.
    services_df.to_html('./services_border_all_columns.html',
                        border=1)

    ######################################################################
    # Upload the lines.html file to S3
    s3.upload_file(Filename='lines.html',
                   # Set the bucket name
                   Bucket='datacamp-public', Key='index.html',
                   # Configure uploaded file
                   ExtraArgs={
                       # Set proper content type
                       'ContentType': 'text/html',
                       # Set proper ACL
                       'ACL': 'public-read'})

    # Print the S3 Public Object URL for the new file.
    print("http://{}.s3.amazonaws.com/{}".format('datacamp-public',
                                                 'index.html'))

    ######################################################################
    df_list = []

    # Load each object from s3
    for file in request_files:
        s3_day_reqs = s3.get_object(Bucket='pat-aws-practice-requests',
                                    Key=file['Key'])
        # Read the DataFrame into pandas, append it to the list
        day_reqs = pd.read_csv(s3_day_reqs['Body'])
        df_list.append(day_reqs)

    # Concatenate all the DataFrames in the list
    all_reqs = pd.concat(df_list)

    # Preview the DataFrame
    all_reqs.head()

    ######################################################################
    # Write agg_df to a CSV and HTML file with no border
    agg_df.to_csv('./feb_final_report.csv')
    agg_df.to_html('./feb_final_report.html', border=0)

    # Upload the generated CSV to the pat-aws-practice-reports bucket
    s3.upload_file(Filename='./feb_final_report.csv',
                   Key='2019/feb/final_report.html',
                   Bucket='pat-aws-practice-reports',
                   ExtraArgs={'ACL': 'public-read'})

    # Upload the generated HTML to the pat-aws-practice-reports bucket
    s3.upload_file(Filename='./feb_final_report.html',
                   Key='2019/feb/final_report.html',
                   Bucket='pat-aws-practice-reports',
                   ExtraArgs={'ContentType': 'text/html',
                              'ACL': 'public-read'})

    ######################################################################
    # List the pat-aws-practice-reports bucket objects starting with 2019/
    objects_list = s3.list_objects(Bucket='pat-aws-practice-reports',
                                   Prefix='2019/')

    # Convert the response contents to DataFrame
    objects_df = pd.DataFrame(objects_list['Contents'])

    # Create a column "Link" that contains Public Object URL
    base_url = "http://pat-aws-practice-reports.s3.amazonaws.com/"
    objects_df['Link'] = base_url + objects_df['Key']

    # Preview the resulting DataFrame
    objects_df.head()

    ######################################################################
    # List the pat-aws-practice-reports bucket objects starting with 2019/
    objects_list = s3.list_objects(Bucket='pat-aws-practice-reports',
                                   Prefix='2019/')

    # Convert the response contents to DataFrame
    objects_df = pd.DataFrame(objects_list['Contents'])

    # Create a column "Link" that contains Public Object URL
    base_url = "http://pat-aws-practice-reports.s3.amazonaws.com/"
    objects_df['Link'] = base_url + objects_df['Key']

    # Preview the resulting DataFrame
    objects_df.head()

    ######################################################################
    # Write objects_df to an HTML file
    objects_df.to_html('report_listing.html',
                       # Set clickable links
                       render_links=True,
                       # Isolate the columns
                       columns=['Link', 'LastModified', 'Size'])

    # Overwrite index.html key by uploading the new file
    s3.upload_file(
        Filename='./report_listing.html', Key='index.html',
        Bucket='pat-aws-practice-reports',
        ExtraArgs={
            'ContentType': 'text/html',
            'ACL': 'public-read'
        })

    ######################################################################
