from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PostState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    normal: _ClassVar[PostState]
    locked: _ClassVar[PostState]
    hidden: _ClassVar[PostState]

class CommentState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    comment_normal: _ClassVar[CommentState]
    comment_hidden: _ClassVar[CommentState]
normal: PostState
locked: PostState
hidden: PostState
comment_normal: CommentState
comment_hidden: CommentState

class id(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class empty_message(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class user(_message.Message):
    __slots__ = ("username",)
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    username: str
    def __init__(self, username: _Optional[str] = ...) -> None: ...

class comment_request(_message.Message):
    __slots__ = ("id", "n")
    ID_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    id: id
    n: int
    def __init__(self, id: _Optional[_Union[id, _Mapping]] = ..., n: _Optional[int] = ...) -> None: ...

class post(_message.Message):
    __slots__ = ("title", "text", "video_url", "image_url", "author", "score", "state", "publication_date", "replies", "post_id")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VIDEO_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    REPLIES_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    title: str
    text: str
    video_url: str
    image_url: str
    author: user
    score: int
    state: PostState
    publication_date: int
    replies: _containers.RepeatedCompositeFieldContainer[id]
    post_id: id
    def __init__(self, title: _Optional[str] = ..., text: _Optional[str] = ..., video_url: _Optional[str] = ..., image_url: _Optional[str] = ..., author: _Optional[_Union[user, _Mapping]] = ..., score: _Optional[int] = ..., state: _Optional[_Union[PostState, str]] = ..., publication_date: _Optional[int] = ..., replies: _Optional[_Iterable[_Union[id, _Mapping]]] = ..., post_id: _Optional[_Union[id, _Mapping]] = ...) -> None: ...

class comment(_message.Message):
    __slots__ = ("post", "comment", "author", "score", "state", "publication_date", "comment_text", "replies", "comment_id")
    POST_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_TEXT_FIELD_NUMBER: _ClassVar[int]
    REPLIES_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    post: id
    comment: id
    author: user
    score: int
    state: CommentState
    publication_date: int
    comment_text: str
    replies: _containers.RepeatedCompositeFieldContainer[id]
    comment_id: id
    def __init__(self, post: _Optional[_Union[id, _Mapping]] = ..., comment: _Optional[_Union[id, _Mapping]] = ..., author: _Optional[_Union[user, _Mapping]] = ..., score: _Optional[int] = ..., state: _Optional[_Union[CommentState, str]] = ..., publication_date: _Optional[int] = ..., comment_text: _Optional[str] = ..., replies: _Optional[_Iterable[_Union[id, _Mapping]]] = ..., comment_id: _Optional[_Union[id, _Mapping]] = ...) -> None: ...

class comment_list(_message.Message):
    __slots__ = ("comments",)
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    comments: _containers.RepeatedCompositeFieldContainer[comment_display]
    def __init__(self, comments: _Optional[_Iterable[_Union[comment_display, _Mapping]]] = ...) -> None: ...

class comment_display(_message.Message):
    __slots__ = ("root_comment", "replies", "has_children")
    ROOT_COMMENT_FIELD_NUMBER: _ClassVar[int]
    REPLIES_FIELD_NUMBER: _ClassVar[int]
    HAS_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    root_comment: comment
    replies: _containers.RepeatedCompositeFieldContainer[comment]
    has_children: bool
    def __init__(self, root_comment: _Optional[_Union[comment, _Mapping]] = ..., replies: _Optional[_Iterable[_Union[comment, _Mapping]]] = ..., has_children: bool = ...) -> None: ...
