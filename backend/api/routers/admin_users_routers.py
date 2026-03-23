from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.users_services import UsersService
from services.admin_logs_services import log_admin_action
from db.schemas.users_schemas import UsersCreate, UsersInfo, UsersUpdate
from core.jwt import get_current_admin_user
from db.models import Users
import logging

log = logging.getLogger(__name__)

router = APIRouter(prefix='/admin/users', tags=['admin_users'])


@router.get("/", response_model=list[UsersInfo])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: bool | None = Query(None),
    is_admin: bool | None = Query(None),
    search: str | None = Query(None, description="Поиск по email, имени, фамилии"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить список всех пользователей с фильтрацией и пагинацией. Требуется админ."""
    service = UsersService(database=db)
    
    # Получаем всех пользователей с пагинацией
    from sqlalchemy import select
    from db.models import Users
    
    query = select(Users).offset(skip).limit(limit)
    
    if is_active is not None:
        query = query.where(Users.is_active == is_active)
    if is_admin is not None:
        query = query.where(Users.is_admin == is_admin)
    if search:
        from sqlalchemy import or_
        query = query.where(
            or_(
                Users.email.ilike(f"%{search}%"),
                Users.first_name.ilike(f"%{search}%"),
                Users.last_name.ilike(f"%{search}%")
            )
        )
    
    res = await db.execute(query)
    users = res.scalars().all()
    
    return [
        UsersInfo(
            id=u.id,
            first_name=u.first_name,
            last_name=u.last_name,
            father_name=u.father_name or None,
            email=u.email,
            is_active=u.is_active,
            is_admin=u.is_admin
        ) for u in users
    ]


@router.get("/count")
async def get_users_count(
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить общее количество пользователей. Требуется админ."""
    from sqlalchemy import func, select
    query = select(func.count(Users.id))
    res = await db.execute(query)
    count = res.scalar()
    return {"total_users": count or 0}


@router.get("/{user_id}", response_model=UsersInfo)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Получить пользователя по ID. Требуется админ."""
    service = UsersService(database=db)
    user = await service.get_user(user_id=user_id)
    return user


@router.post("/", response_model=UsersInfo)
async def create_user(
    user_data: UsersCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Создать нового пользователя. Требуется админ."""
    service = UsersService(database=db)
    user = await service.create_user(data=user_data)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="CREATE",
        entity="users",
        entity_id=user.id,
        description=f"Создан пользователь {user.email}",
        ip_address=request.client.host if request.client else None
    )
    
    return user


@router.put("/{user_id}", response_model=UsersInfo)
async def update_user(
    user_id: int,
    data: UsersUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Обновить пользователя. Требуется админ."""
    service = UsersService(database=db)
    user = await service.update_user(user_id=user_id, data=data)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="UPDATE",
        entity="users",
        entity_id=user_id,
        description=f"Обновлен пользователь {user.email}",
        ip_address=request.client.host if request.client else None
    )
    
    return user


@router.patch("/{user_id}/status")
async def update_user_status(
    user_id: int,
    request: Request,
    is_active: bool = Query(...),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Обновить статус пользователя (активен/не активен). Требуется админ."""
    service = UsersService(database=db)
    user = await service.udpate_status_user(user_id=user_id, status=is_active)

    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="UPDATE",
        entity="users",
        entity_id=user_id,
        description=f"Статус пользователя {user.email} изменён на {is_active}",
        ip_address=request.client.host if request.client else None
    )

    return {"message": f"Статус пользователя изменён на {is_active}", "user_id": user_id}


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Удалить пользователя. Требуется админ."""
    service = UsersService(database=db)
    result = await service.delete_user(user_id=user_id)
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="DELETE",
        entity="users",
        entity_id=user_id,
        description=f"Удалён пользователь с ID {user_id}",
        ip_address=request.client.host if request.client else None
    )
    
    return result


@router.delete("/batch")
async def batch_delete_users(
    request: Request,
    user_ids: list[int] = Query(..., description="Список ID пользователей для удаления"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin_user)
):
    """Массовое удаление пользователей. Требуется админ."""
    service = UsersService(database=db)
    deleted_count = 0
    
    for uid in user_ids:
        try:
            await service.delete_user(user_id=uid)
            deleted_count += 1
        except Exception as e:
            log.error(f"Не удалось удалить пользователя {uid}: {e}")
    
    # Логирование
    await log_admin_action(
        db=db,
        admin_id=current_admin.id,
        action="DELETE",
        entity="users",
        description=f"Массовое удаление: удалено {deleted_count} из {len(user_ids)} пользователей",
        ip_address=request.client.host if request.client else None
    )
    
    return {"message": f"Удалено {deleted_count} из {len(user_ids)} пользователей", "deleted_count": deleted_count}
