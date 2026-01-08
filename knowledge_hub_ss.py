"""
KHSS Backend - Main Entry Point
FastAPI application with Supabase integration
"""
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# ================== CONFIGURATION ==================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "secret")

# Initialize Supabase client (shared across modules)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================== FASTAPI APP ==================
app = FastAPI(title="KHSS Backend API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================== DEPENDENCIES ==================
async def verify_admin_token(x_admin_token: str = Header(...)):
    """Verify admin token for protected endpoints"""
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    return x_admin_token

# ================== HEALTH CHECK ==================
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ================== KNOWLEDGE HUB ROUTES (INLINE) ==================
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class KnowledgeHubResponse(BaseModel):
    id: int
    slug: str
    title: str
    content: str
    summary: Optional[str] = None
    life_stage_id: Optional[int] = None
    perspective_id: Optional[int] = None
    author_name: Optional[str] = None
    read_time_minutes: int = 5
    is_featured: bool = False
    published_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

@app.get("/api/knowledge-hub/", response_model=List[KnowledgeHubResponse], tags=["knowledge-hub"])
def get_knowledge_hub_items(
    lang: str = "en",
    life_stage_id: int | None = None,
    perspective_id: int | None = None,
    life_stage: int | None = None,
    perspective: int | None = None,
    lifeStage: int | None = None,
    is_featured: bool | None = None,
    perPage: int = 100,
    search: str | None = None
):
    """Get all knowledge hub items with language support and filtering"""
    # Support multiple parameter naming conventions
    ls_id = life_stage_id if life_stage_id is not None else (life_stage if life_stage is not None else lifeStage)
    p_id = perspective_id if perspective_id is not None else perspective
    
    query = supabase.table("sakhi_knowledge_hub").select("*")

    if search:
        query = query.ilike("title", f"%{search}%")
    
    if ls_id is not None:
        query = query.eq("life_stage_id", ls_id)
    if p_id is not None:
        query = query.eq("perspective_id", p_id)
    if is_featured is not None:
        query = query.eq("is_featured", is_featured)
        
    response = query.order("published_at", desc=True).limit(perPage).execute()
    
    items = []
    for item in response.data:
        if lang == "te":
            item["title"] = item.get("title_te") or item.get("title")
            item["summary"] = item.get("summary_te") or item.get("summary")
            item["content"] = item.get("content_te") or item.get("content")
        items.append(KnowledgeHubResponse.model_validate(item))
        
    return items

@app.get("/api/knowledge-hub/{slug}", response_model=KnowledgeHubResponse, tags=["knowledge-hub"])
def get_knowledge_hub_item_by_slug(slug: str, lang: str = "en"):
    """Get a single knowledge hub item by slug with language support"""
    response = supabase.table("sakhi_knowledge_hub").select("*").eq("slug", slug).limit(1).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Knowledge Hub item not found")
    
    item = response.data[0]
    if lang == "te":
        item["title"] = item.get("title_te") or item.get("title")
        item["summary"] = item.get("summary_te") or item.get("summary")
        item["content"] = item.get("content_te") or item.get("content")
        
    return KnowledgeHubResponse.model_validate(item)

# ================== SUCCESS STORIES ROUTES (INLINE) ==================
from uuid import UUID
from enum import Enum
from pydantic import Field, model_validator
from fastapi import Depends, UploadFile, File
import uuid as uuid_module

class ShareType(str, Enum):
    NAMED = "named"
    ANONYMOUS = "anonymous"

class StoryStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    PUBLISHED = "published"

class StoryBase(BaseModel):
    share_type: ShareType
    name: Optional[str] = None
    city: str = Field(min_length=1)
    journey_duration: str = Field(min_length=1)
    challenges: str = Field(min_length=1)
    emotions: List[str] = Field(min_length=1)
    treatments: List[str] = Field(min_length=1)
    emotion_description: Optional[str] = None
    journey_outcome: str = Field(min_length=1)
    more_details: Optional[str] = None
    hope_message: Optional[str] = None
    photo_url: Optional[str] = None
    summary: Optional[str] = None
    generated_story: Optional[str] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    stage: Optional[str] = None
    language: str = "en"

    @model_validator(mode='after')
    def check_name_if_named(self):
        if self.share_type == ShareType.NAMED and not self.name:
            raise ValueError('name is required when share_type is named')
        return self

class StoryCreate(StoryBase):
    pass

class StoryUpdateStatus(BaseModel):
    status: StoryStatus

class StoryConsent(BaseModel):
    id: UUID

class StoryResponse(StoryBase):
    id: UUID
    status: str
    consent: bool
    created_at: str

    class Config:
        from_attributes = True

TABLE_NAME = "sakhi_success_stories"

@app.post("/stories/draft", response_model=StoryResponse, status_code=status.HTTP_201_CREATED, tags=["stories"])
async def create_story_draft(story_in: StoryCreate):
    """Create a new story draft"""
    data = story_in.model_dump()
    data["status"] = "pending"
    data["consent"] = False
    response = supabase.table(TABLE_NAME).insert(data).execute()
    return StoryResponse.model_validate(response.data[0])

@app.post("/stories/consent", response_model=StoryResponse, tags=["stories"])
async def record_consent(consent_in: StoryConsent):
    """Record user consent for a story"""
    response = supabase.table(TABLE_NAME).update({"consent": True}).eq("id", str(consent_in.id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Story not found")
    return StoryResponse.model_validate(response.data[0])

@app.get("/stories/", response_model=List[StoryResponse], tags=["stories"])
async def get_published_stories():
    """Get all published stories"""
    response = supabase.table(TABLE_NAME).select("*").eq("status", "published").order("created_at", desc=True).execute()
    return [StoryResponse.model_validate(item) for item in response.data]

@app.get("/stories/{id}", response_model=StoryResponse, tags=["stories"])
async def get_story_by_id(id: UUID):
    """Get a story by ID"""
    response = supabase.table(TABLE_NAME).select("*").eq("id", str(id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Story not found")
    return StoryResponse.model_validate(response.data[0])

@app.put("/stories/{id}/status", response_model=StoryResponse, tags=["stories"])
async def update_story_status(
    id: UUID,
    status_in: StoryUpdateStatus,
    token: str = Depends(verify_admin_token)
):
    """Update story status (admin only)"""
    response = supabase.table(TABLE_NAME).update({"status": status_in.status}).eq("id", str(id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Story not found")
    return StoryResponse.model_validate(response.data[0])

@app.post("/stories/upload", status_code=status.HTTP_201_CREATED, tags=["stories"])
async def upload_photo(photo: UploadFile = File(...)):
    """Upload a photo for a story"""
    unique_name = f"{uuid_module.uuid4()}-{photo.filename}".replace(" ", "-")
    base_url = "https://example-bucket.s3.amazonaws.com/uploads"
    return {"photo_url": f"{base_url}/{unique_name}"}
