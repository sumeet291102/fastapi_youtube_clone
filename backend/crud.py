from sqlalchemy.orm import Session, joinedload, subqueryload

from . import models, schemas


def get_user(db: Session, username: str):
    user = db.query(models.User).options(joinedload(models.User.videos)).filter(models.User.username == username).first()
    return user


def get_user_by_id(db: Session, id: int):
    user = db.query(models.User).options(joinedload(models.User.videos)).filter(models.User.id == id).first()
    return user


def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(username=user.username, email=user.email, first_name=user.first_name, last_name=user.last_name, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user: schemas.UserUpdate):
    updated_user = db.query(models.User).filter(models.User.username == user.username).first()
    if user.profile_cover:
        updated_user.profile_cover = user.profile_cover
    if user.profile_pic:
        updated_user.profile_pic = user.profile_pic
    if user.user_description:
        updated_user.user_description = user.user_description
    db.commit()


# ------------------------------------------------------------------------------------------------------------------


def create_video(db: Session, user_id: int, video: schemas.VideoCreate):
    video = models.Video(title=video.title, description=video.description, url=video.url, uploaded_by_id=user_id)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video


def get_video(db: Session, video_id: int):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    return video


def get_videos(db: Session):
    videos = db.query(models.Video).all()
    return videos

# ------------------------------------------------------------------------------------------------------------------


def create_like(db: Session, user_id: int, video_id: int):

    already_liked = db.query(models.Like).filter(models.Like.liked_by_id == user_id, models.Like.liked_on_id == video_id).first()

    if already_liked:
        db.query(models.Like).filter(models.Like.liked_by_id == user_id, models.Like.liked_on_id == video_id).delete()
        db.commit()
        return {'msg': 'removed like'}
    else:
        like = models.Like(liked_by_id=user_id, liked_on_id=video_id)
        db.add(like)
        db.commit()
        db.refresh(like)
        return like


def get_like(db: Session, user_id: int, video_id: int):
    like = db.query(models.Like).filter(models.Like.liked_by_id == user_id, models.Like.liked_on_id == video_id).first()
    if like:
        return True
    else:
        return False


def get_likes(db: Session, video_id: int):
    likes = db.query(models.Like).filter(models.Like.liked_on_id == video_id)
    return len(list(likes))

# ------------------------------------------------------------------------------------------------------------------


def create_comment(db: Session, user_id: int, video_id: int, comment: schemas.CommentCreate):
    comment = models.Comment(content=comment.content, commented_by_id=user_id, commented_on_id=video_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments(db: Session, video_id: int):
    comments = db.query(models.Comment).filter(models.Comment.commented_on_id == video_id)
    return comments

# ------------------------------------------------------------------------------------------------------------------


def create_subscriber(db: Session, subscriber_id: int, subscribee_id: int):
    already_subscribed = db.query(models.Subscriber).filter(models.Subscriber.subscriber_id == subscriber_id, models.Subscriber.subscribee_id == subscribee_id).first()
    if already_subscribed:
        db.query(models.Subscriber).filter(models.Subscriber.subscriber_id == subscriber_id, models.Subscriber.subscribee_id == subscribee_id).delete()
        db.commit()
        return {'msg': 'removed subscriber'}
    else:
        subscriber = models.Subscriber(subscriber_id=subscriber_id, subscribee_id=subscribee_id)
        db.add(subscriber)
        db.commit()
        db.refresh(subscriber)
        return subscriber


def get_subscribers(db: Session, subscribee_id: int):
    subscribers = db.query(models.Subscriber).filter(models.Subscriber.subscribee_id == subscribee_id)
    return len(list(subscribers))


def get_subscriber(db: Session, subscriber_id: int, subscribee_id: int):
    subscriber = db.query(models.Subscriber).filter(models.Subscriber.subscriber_id == subscriber_id, models.Subscriber.subscribee_id == subscribee_id).first()
    if subscriber:
        return True
    else:
        return False