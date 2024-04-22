from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# replace it with your 32 bit secret key
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

# encryption algorithm
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post('/login/')
def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_data.username, models.User.password == user_data.password).first()
    if not user:
        return "fail"

    user_dict = {}
    for attribute in user.__table__.columns:
        user_dict[attribute.name] = str(getattr(user, attribute.name))

    token = create_access_token(user_dict)
    return token


@app.post('/signup/')
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        return "fail"
    else:
        return crud.create_user(db, user)


@app.get('/user/')
def get_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        user_obj = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
    return crud.get_user(db, user_obj['username'])


@app.get('/user_by_id/{id}')
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, id)


@app.get('/user/{username}')
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    return crud.get_user(db, username)


@app.post('/user/')
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db, user)

# ----------------------------------------------------------------------------------------------


@app.get('/video/', response_model=list[schemas.Video])
def get_videos(db: Session = Depends(get_db)):
    return crud.get_videos(db)


@app.get('/video/{video_id}', response_model=schemas.Video)
def get_video(video_id: int, db: Session = Depends(get_db)):
    return crud.get_video(db, video_id)


@app.post('/video/', response_model=schemas.Video)
def create_video(video: schemas.VideoCreate, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        user_obj = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = crud.get_user(db, user_obj['username'])
    except JWTError:
        return None
    return crud.create_video(db, user.id, video)

# ----------------------------------------------------------------------------------------------


@app.get('/like/{video_id}', response_model=bool)
def get_like(video_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        user_obj = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = crud.get_user(db, user_obj['username'])
    except JWTError:
        return False
    return crud.get_like(db, user.id, video_id)

@app.get('/likes/{video_id}', response_model=int)
def get_likes(video_id: int, db: Session = Depends(get_db)):
    return crud.get_likes(db, video_id)

@app.post('/like/{video_id}')
def create_like(video_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        user_obj = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = crud.get_user(db, user_obj['username'])
    except JWTError:
        return None
    return crud.create_like(db, user.id, video_id)

# ----------------------------------------------------------------------------------------------

@app.get('/comments/{video_id}', response_model=list[schemas.Comment])
def get_comments(video_id: int, db: Session = Depends(get_db)):
    return crud.get_comments(db, video_id)

@app.post('/comment/{video_id}', response_model=schemas.Comment)
def create_comment(video_id: int, comment: schemas.CommentCreate, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        user_obj = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = crud.get_user(db, user_obj['username'])
    except JWTError:
        return None
    return crud.create_comment(db, user.id, video_id, comment)

# ----------------------------------------------------------------------------------------------



@app.get('/subscriber/{subscribee_id}', response_model=bool)
def get_subscriber(subscribee_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        user_obj = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = crud.get_user(db, user_obj['username'])
    except JWTError:
        return False
    return crud.get_subscriber(db, user.id, subscribee_id)


@app.get('/subscribers/{subscribee_id}', response_model=int)
def get_subscribers(subscribee_id: int, db: Session = Depends(get_db)):
    return crud.get_subscribers(db, subscribee_id)


@app.post('/subscriber/{subscribee_id}')
def create_subscriber(subscribee_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        user_obj = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = crud.get_user(db, user_obj['username'])
    except JWTError:
        return None
    return crud.create_subscriber(db, user.id, subscribee_id)