import a3_pb2
import high_level_function

def test(client):

    post = a3_pb2.post(title="First post",\
                       text="Nothing to see here",\
                        video_url=None,\
                            image_url=None,\
                                author=a3_pb2.user(username="Iam Thespy"),\
                                    score=None,\
                                        state=a3_pb2.PostState.normal,\
                                            publication_date=100,\
                                                replies=None,\
                                                    post_id=None)
    p1 = client.CreatePost(post)
    p1c1 = client.CreateCommment(a3_pb2.comment(post=p1,author=a3_pb2.user(username="Iam Thespy"),state=a3_pb2.CommentState.comment_normal,\
                                              comment_text="Nothing to see here"))
    
    p1c1r1 = client.CreateCommment(a3_pb2.comment(comment=p1c1,author=a3_pb2.user(username="Iam Thespy"),state=a3_pb2.CommentState.comment_normal,\
                                              comment_text="Something to see here"))
    return high_level_function.high_level_function(client,p1)