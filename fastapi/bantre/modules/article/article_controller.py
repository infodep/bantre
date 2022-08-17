# from fastapi import APIRouter, Depends
# from pydantic import BaseModel
# from sqlmodel import Session

# from bantre.modules.article.article_model import ArticleModel
# from bantre.util.auth import User, token_required
# from bantre.database import get_session

# article_router = APIRouter()


# class ArticleBase(BaseModel):
#     id: int
#     title: str
#     text_source: str
#     image: str


# class ArticleCreate(ArticleBase):
#     pass


# class Article(ArticleBase):
#     # This is the text converted to html from markdown
#     text: str

#     # This is necessary for the pydantic schema to work with the ORM
#     class Config:
#         orm_mode = True


# @article_router.get("/")
# def get_all_articles(
#     current_user: User = Depends(token_required), session: Session = Depends(get_session)
# ):
#     current_user
#     query = select(ArticleModel).order_by(ArticleModel.touched)
#     result = session.execute(query)
#     return result.all()
