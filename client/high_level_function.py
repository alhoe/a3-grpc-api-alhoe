import a3_pb2

def high_level_function(client, post_id):
    n=1
    post = client.GetPostContent(post_id)
    N_top_comments = client.GetNComments(a3_pb2.comment_request(id=post_id,n=n))
    
    if N_top_comments.comments[0].has_children:
        most_upvoted_comment_id = N_top_comments.comments[0].root_comment.comment_id
        N_top_replies = client.GetNComments(a3_pb2.comment_request(id=most_upvoted_comment_id,n=n))
        return N_top_replies.comments[0].root_comment.comment_text
    else:
        None