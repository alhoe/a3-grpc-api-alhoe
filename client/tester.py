import a3_pb2
import a3_pb2_grpc
import high_level_function
from unittest.mock import MagicMock

class FakeClass():
    def fake():
        return 0

client = FakeClass()
client.GetPostContent =  MagicMock(return_value = a3_pb2.post())
client.GetNComments = MagicMock(return_value = a3_pb2.comment_list(comments=[a3_pb2.comment_display()]))
client.CreatePost = MagicMock(return_value = a3_pb2.id(id=42))
client.CreateCommment = MagicMock(return_value=a3_pb2.id(id=43))

def test(client):
    print("Starting Test")
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
    print("Post created")
    p1c1 = client.CreateCommment(a3_pb2.comment(post=p1,author=a3_pb2.user(username="Iam Thespy"),state=a3_pb2.CommentState.comment_normal,\
                                              comment_text="Nothing to see here"))
    print("Comment Created")
    p1c1r1 = client.CreateCommment(a3_pb2.comment(comment=p1c1,author=a3_pb2.user(username="Iam Thespy"),state=a3_pb2.CommentState.comment_normal,\
                                              comment_text="Something to see here"))
    
    print("Test setup complete")
    return high_level_function.high_level_function(client,p1)

test(client)