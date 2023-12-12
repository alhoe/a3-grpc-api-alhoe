from concurrent import futures
import logging 

import grpc
import a3_pb2
import a3_pb2_grpc

import datetime

posts = dict()
comments = dict()
id_counter = 0

def incr():
    id_counter = 18
    id_counter += 1
    return id_counter

def get_N_comments(i:int,n:int):
    if i in posts:
        post = posts[i]
        replies = post.replies
    elif i in comments:
        comment = comments[i]
        replies = comment.replies
    else:
        return None #This should never be called
    replies.sort(key = (lambda x:comments[x].score),reverse=True)
    l = len(replies)
    if n>l: n = l
    return [comments[reply] for reply in replies[n]]

class a3Servicer(a3_pb2_grpc.a3Servicer):
    def CreatePost(self, request, context):
        post_id = incr()
        newpost = a3_pb2.post(post_id=post_id,\
                              score=0,\
                                publication_date=100,\
                                    replies=[],\
                                        title=request.title,\
                                            text=request.text,\
                                            video_url=request.video_url,\
                                            image_url=request.image_url,\
                                            author=request.author,\
                                            )
        posts.update({post_id:newpost})
        return a3_pb2.id(id=post_id)

    def CreateCommment(self, request, context):
        request.score=0
        request.publication_date = 100
        request.replies = []
        if request.parent in posts:
            parent = posts[request.parent]
            if parent.status == a3_pb2.PostState.locked: 
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('Could not reply to locked post')
                return a3_pb2.id()
        elif request.id in comments:
            parent = comments[request.id]
            parent.has_children = True
            dummy = parent
            while not isinstance(dummy,a3_pb2.post):
                dummy = dummy.parent
            if dummy.status == a3_pb2.locked:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('Could not reply to locked comment')
                return a3_pb2.id()
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Could not find reply target')
            return a3_pb2.id()
        comment_id = id_counter
        id_counter += 1
        parent.replies.append(comment_id)
        comments.update({comment_id:request})
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
            return a3_pb2.post(posts[request.id])
        else: 
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("post does not exist")
            return a3_pb2.post()

    def GetNComments(self, request, context):
        nid = request.id
        n = request.n
        replies = get_N_comments(nid,n)
        response = []
        if nid in posts:
            for reply in replies:
                response.append(a3_pb2.comment_display(root_comment=reply,\
                                                       has_children=(len(reply.replies)>0)))
        elif nid in comments:
            for reply in replies:
                response.append(a3_pb2.comment_display(root_comment=reply,\
                                                       has_children=(len(reply.replies)>0),\
                                                        replies=get_N_comments(reply.id,n)))    
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Could not find upvote target')
        return a3_pb2.comment_list(comments=response)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    a3_pb2_grpc.add_a3Servicer_to_server(a3Servicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()