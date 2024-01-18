import re
def extract_comments(input_string):
    comments_dict = {}

    # Split the input string into lines based on "1. ", "2. ", etc.
    total_reponse = input_string.split("Review Comments:")
    fetching_review = total_reponse[1]
    print(fetching_review)
    overallFeedback = fetching_review.split("Overall Feedback:")
    fileFeedback = overallFeedback[-1]
    fetching_review_lines = overallFeedback[0]
    feedback_list = re.split(r'(\d+\.)',fetching_review_lines)
    p =[]
    for i in feedback_list:
        if("Line" in i):
            p.append(i)
    print(p)
    result_dict = {}

    for item in p:
        match = re.match(r'\s*(.*?):\s*(.*)', item)
        if match:
            key, value = match.groups()
            result_dict[key.strip()] = value.strip()
    print(result_dict)
    print(fileFeedback)


# ['1. Line 6', ' Comment for CodeDialog Box The comment // test the codeDialog box lacks clarity. Consider pr
# oviding a more descriptive comment to explain the purpose or functionality. 2. Lines 10-12', ' For Loop The
# loop seems fine, but consider adding braces {} around the loop body for better code consistency and to avoid
#  potential issues in the future. Overall Feedback', "The addition of the for loop is acceptable, but conside
# r adding braces around the loop body for consistency. Improve the clarity of the comment on Line 6 for bette
# r understanding of the code's purpose. The provided feedback focuses on improving clarity and maintaining co
# nsistency in the code."]

# Given input string
input_string = "python code \n Review Comments:1. Line 6: Comment for CodeDialog Box The comment // test the codeDialog box lacks clarity. Consider providing a more descriptive comment to explain the purpose or functionality. 2. Lines 10-12: For Loop The loop seems fine, but consider adding braces {} around the loop body for better code consistency and to avoid potential issues in the future. Overall Feedback:The addition of the for loop is acceptable, but consider adding braces around the loop body for consistency. Improve the clarity of the comment on Line 6 for better understanding of the code's purpose. The provided feedback focuses on improving clarity and maintaining consistency in the code."

# Extract comments and print the result
comments_result = extract_comments(input_string)
print(comments_result)
