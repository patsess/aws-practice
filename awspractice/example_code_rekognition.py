
import boto3

"""
Note: code is for reference only (taken from an online course)
"""


if __name__ == '__main__':
    # Generate the boto3 client for interacting with rekognition (for image
    # recognition)
    rekog = boto3.client('rekognition', region_name='us-east-1',
                         # Set up AWS credentials
                         aws_access_key_id=AWS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET)

    ######################################################################
    # Use Rekognition client to detect labels
    image1_response = rekog.detect_labels(
        # Specify the image as an S3Object; Return one label
        Image=image1, MaxLabels=1)

    # Print the labels
    print(image1_response['Labels'])

    ######################################################################
    # Create an empty counter variable
    cats_count = 0
    # Iterate over the labels in the response
    for label in response['Labels']:
        # Find the cat label, look over the detected instances
        if label['Name'] == 'Cat':
            for instance in label['Instances']:
                # Only count instances with confidence > 85
                if (instance['Confidence'] > 85):
                    cats_count += 1

    # Print count of cats
    print(cats_count)

    ######################################################################
    # Create empty list of words
    words = []
    # Iterate over the TextDetections in the response dictionary
    for text_detection in response['TextDetections']:
        # If TextDetection type is WORD, append it to words list
        if text_detection['Type'] == 'WORD':
            # Append the detected text
            words.append(text_detection['DetectedText'])

    # Print out the words list
    print(words)

    ######################################################################
