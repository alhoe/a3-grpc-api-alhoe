import a3_pb2

def high_level_function(client, post_id):
    n=1
    post = client.GetPostContent(a3_pb2.id(post_id))
    N_top_comments = client.get_N_comments(a3_pb2.comment_request(id=post_id,n=n))
    
    if N_top_comments[0].has_children:
        most_upvoted_comment_id = N_top_comments[0].root_comment.id
        N_top_replies = client.get_N_comments(a3_pb2.comment_request(id=most_upvoted_comment_id,n=n))
        return N_top_replies[0].root_comment
    else:
        None