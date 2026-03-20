from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.agent import AgentCreate, AgentRead, AgentUpdate
from backend.db.models.models import Agent
from db.session import get_db
from core.dependencies import require_role