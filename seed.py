import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy.future import select
from app.db.session import AsyncSessionLocal
from app.models.user import User, RoleEnum
from app.models.consultation import Consultation, StatusEnum
from app.core.security import hash_password

async def seed_data():
    async with AsyncSessionLocal() as db:
        # Create Users
        users_data = [
            {"email": "consultant@example.com", "password": "password123", "full_name": "Dr. Smith", "role": RoleEnum.consultant},
            {"email": "client1@example.com", "password": "password123", "full_name": "Alice Johnson", "role": RoleEnum.client},
            {"email": "client2@example.com", "password": "password123", "full_name": "Bob Williams", "role": RoleEnum.client},
        ]
        
        users = {}
        for u_data in users_data:
            result = await db.execute(select(User).where(User.email == u_data["email"]))
            user = result.scalars().first()
            if not user:
                user = User(
                    email=u_data["email"],
                    hashed_password=hash_password(u_data["password"]),
                    full_name=u_data["full_name"],
                    role=u_data["role"],
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)
            users[u_data["role"].value if u_data["role"] == RoleEnum.consultant else u_data["email"]] = user

        # Create Consultations
        consultant = users["consultant"]
        client1 = users["client1@example.com"]
        client2 = users["client2@example.com"]
        
        consultations_data = [
            {"client_id": client1.id, "consultant_id": consultant.id, "scheduled_at": datetime.now(timezone.utc) + timedelta(days=1), "duration_minutes": 60, "status": StatusEnum.pending, "notes": "Initial consultation"},
            {"client_id": client1.id, "consultant_id": consultant.id, "scheduled_at": datetime.now(timezone.utc) + timedelta(days=2), "duration_minutes": 30, "status": StatusEnum.confirmed, "notes": "Follow-up"},
            {"client_id": client2.id, "consultant_id": consultant.id, "scheduled_at": datetime.now(timezone.utc) - timedelta(days=1), "duration_minutes": 45, "status": StatusEnum.completed, "notes": "Completed session"},
            {"client_id": client2.id, "consultant_id": consultant.id, "scheduled_at": datetime.now(timezone.utc) + timedelta(days=3), "duration_minutes": 60, "status": StatusEnum.cancelled, "notes": "Cancelled by client"},
        ]
        
        # Check if consultations exist for the consultant
        result = await db.execute(select(Consultation).where(Consultation.consultant_id == consultant.id))
        existing_consultations = result.scalars().all()
        
        if not existing_consultations:
            for c_data in consultations_data:
                consultation = Consultation(**c_data)
                db.add(consultation)
            await db.commit()
            print("Database seeded successfully with users and consultations.")
        else:
            print("Database already contains consultations. Skipping seed.")

if __name__ == "__main__":
    asyncio.run(seed_data())
