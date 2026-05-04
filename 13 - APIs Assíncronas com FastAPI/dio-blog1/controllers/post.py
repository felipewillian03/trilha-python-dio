from typing_extensions import Annotated
from fastapi import Response, Cookie, status, Header, APIRouter
from datetime import UTC, datetime
from pydantic import BaseModel

# Definição dos modelos (já que não encontrou os imports)
class PostIn(BaseModel):
    title: str
    published: bool = False

class PostOut(BaseModel):
    title: str
    date: datetime
    published: bool

router = APIRouter(prefix="/posts")

fake_db = [  
    {"title": "Criando uma aplicação com Django", "date": datetime.now(UTC), 'published': True},
    {"title": "Internacionalizando uma app FastAPI", "date": datetime.now(UTC), 'published': True},
    {"title": "Internacionalizando uma app Flask", "date": datetime.now(UTC), 'published': True},
    {"title": "Internacionalizando uma app Starlett", "date": datetime.now(UTC), 'published': False},
]

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostOut)
def create_post(post: PostIn):
    fake_db.append(post.model_dump())
    # ✅ Retornar objeto PostOut
    return PostOut(**post.model_dump(), date=datetime.now(UTC))

@router.get("/", response_model=list[PostOut])
def read_posts(
    response: Response,
    published: bool,
    limit: int, 
    skip: int = 0, 
    ads_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None
):
    response.set_cookie(key="ads_id", value="viroska@viroska.com")
    print(f"Cookie: {ads_id}")
    print(f"User-Agent: {user_agent}")
    tail = skip + limit
    
    # ✅ Filtrar e converter para PostOut
    filtered_posts = [post for post in fake_db[skip:tail] if post['published'] == published]
    return [PostOut(**post) for post in filtered_posts]

@router.get("/{framework}")  # ← Sem response_model
def read_framework_posts(framework: str):
    return {
        "posts": [  
            {"title": f"Criando uma aplicação com {framework}", "date": datetime.now(UTC)},
            {"title": f"Internacionalizando uma app {framework}", "date": datetime.now(UTC)},
        ]
    }