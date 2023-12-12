from concurrent import futures
import logging 

import grpc
import a3_pb2
import a3_pb2_grpc

import datetime

posts = dict()
comments = dict()

def get_N_comments(i,n:int):
    i = i.id
    if i in posts:
        post = posts[i]
        replies = post.replies
    elif i in comments:
        comment = comments[i]
        replies = comment.replies
    else:
        return None #This should never be called
    replies.sort(key = (lambda x:comments[x.id].score),reverse=True)
    l = len(replies)
    if n>l: n = l
    return [comments[reply.id] for reply in replies[0:n]]

class a3(a3_pb2_grpc.a3Servicer):
    def __init__(self):
        self.id_counter = 0

    def incr(self):
        self.id_counter += 1
        return self.id_counter
    
    def CreatePost(self, request, context):
        post_id = self.incr()
        newpost = a3_pb2.post(title="First post",\
                       text=request.text,\
                        video_url=request.video_url,\
                            image_url=request.image_url,\
                                author=request.author,\
                                    score=0,\
                                        state=request.state,\
                                            publication_date=100,\
                                                replies=[],\
                                                    post_id=a3_pb2.id(id=post_id)
                                            )
        posts.update({post_id:newpost})
        return a3_pb2.id(id=post_id)

    def CreateCommment(self, request, context):
        comment_id = self.incr()
        newcomment = a3_pb2.comment(post=request.post,\
                                    comment=request.comment,\
                                        author=request.author,\
                                            score=0,\
                                                state=request.state,\
                                                    publication_date=100,\
                                                        comment_text=request.comment_text,\
                                                            replies=[],\
                                                                comment_id=a3_pb2.id(id=comment_id))
        if request.post != None and request.post.id in posts:
            parent = posts[request.post.id]
            if parent.state == a3_pb2.PostState.locked: 
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('Could not reply to locked post')
                return a3_pb2.id()
        elif request.comment != None and request.comment.id in comments:
            parent = comments[request.comment.id]
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Could not find reply target')
            return a3_pb2.id()
        parent.replies.append(a3_pb2.id(id=comment_id))
        comments.update({comment_id:newcomment})
        return a3_pb2.id(id=comment_id)

    def Upvote(self, request, context):
        upid = request.id
        if upid in posts:
            post = posts[request.id]
            post.score += 1
        elif upid in comments:
            comment = comments[request.id]
            comment.score += 1
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Could not find upvote target')
        return a3_pb2.empty_message()

    def Downvote(self, request, context):
        downid = request.id
        if downid in posts:
            post = posts[request.id]
            post.score -= 1
        elif downid in comments:
            comment = comments[request.id]
            comment.score -= 1
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Could not find downvote target')
        return a3_pb2.empty_message()

    def GetPostContent(self, request, context):
        if request.id in posts:
            return posts[request.id]
        else: 
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("post does not exist")
            return a3_pb2.post()

    def GetNComments(self, request, context):
        nid = request.id
        n = request.n
        replies = get_N_comments(nid,n)
        response = []
        nid = request.id.id
        if nid in posts:
            for reply in replies:
                response.append(a3_pb2.comment_display(root_comment=reply,\
                                                       has_children=(len(reply.replies)>0)))
        elif nid in comments:
            for reply in replies:
                response.append(a3_pb2.comment_display(root_comment=reply,\
                                                       has_children=(len(reply.replies)>0),\
                                                        replies=get_N_comments(reply.comment_id,n)))    
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'Could not find comment id {nid}')
        return a3_pb2.comment_list(comments=response)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    a3_pb2_grpc.add_a3Servicer_to_server(a3(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    print("Server started, listening on " + "localhost:50051")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()