"""
Database seeder script using asyncpg.
"""
import asyncio
import asyncpg
import uuid
import random
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.core.config import settings

# Setup bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
DEFAULT_PASSWORD = "password123"
HASHED_PASSWORD = pwd_context.hash(DEFAULT_PASSWORD)

async def seed():
    print("Connecting to DB...")
    # Make sure we use the asyncpg dialect in the DSN, or just standard postgresql URL
    dsn = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    
    conn = await asyncpg.connect(dsn)
    try:
        # Check if already seeded
        val = await conn.fetchval("SELECT COUNT(*) FROM users")
        if val > 0:
            print("Database already contains users. Skipping seed to maintain idempotency.")
            return

        print("Seeding users...")
        consultants = [
            (str(uuid.uuid4()), "Alice Chen", "alice@example.com", "consultant"),
            (str(uuid.uuid4()), "Bob Martinez", "bob@example.com", "consultant"),
            (str(uuid.uuid4()), "Carol White", "carol@example.com", "consultant"),
        ]
        
        clients = [
            (str(uuid.uuid4()), "David Lee", "david@example.com", "client"),
            (str(uuid.uuid4()), "Emma Johnson", "emma@example.com", "client"),
            (str(uuid.uuid4()), "Frank Brown", "frank@example.com", "client"),
            (str(uuid.uuid4()), "Grace Kim", "grace@example.com", "client"),
            (str(uuid.uuid4()), "Henry Davis", "henry@example.com", "client"),
        ]

        users = consultants + clients
        for uid, name, email, role in users:
            await conn.execute(
                '''INSERT INTO users (id, name, email, role, hashed_password) 
                   VALUES ($1, $2, $3, $4, $5)''',
                uid, name, email, role, HASHED_PASSWORD
            )

        print("Seeding consultations...")
        consultation_data = []
        statuses = ["pending", "confirmed", "completed", "cancelled"]
        
        for i in range(10):
            client = random.choice(clients)
            consultant = random.choice(consultants)
            status = random.choice(statuses)
            scheduled_at = datetime.now(timezone.utc) + timedelta(days=random.randint(-10, 10))
            cid = str(uuid.uuid4())
            consultation_data.append((cid, client[0], consultant[0], scheduled_at, status))
            
            await conn.execute(
                '''INSERT INTO consultations (id, client_id, consultant_id, scheduled_at, status, notes) 
                   VALUES ($1, $2, $3, $4, $5, $6)''',
                cid, client[0], consultant[0], scheduled_at, status, f"Notes for consultation {i}"
            )

        print("Seeding transactions...")
        transaction_data = []
        for cid, _, _, _, status in consultation_data:
            tid = str(uuid.uuid4())
            amount = round(random.uniform(50.0, 500.0), 2)
            t_status = "paid" if status == "completed" else ("pending" if status in ["pending", "confirmed"] else "refunded")
            transaction_data.append((tid, cid, amount, t_status))
            
            await conn.execute(
                '''INSERT INTO transactions (id, consultation_id, amount, currency, status) 
                   VALUES ($1, $2, $3, 'USD', $4)''',
                tid, cid, amount, t_status
            )

        print("Seeding reviews...")
        # Reviews only for completed consultations
        completed_consultations = [c for c in consultation_data if c[4] == "completed"]
        
        review_count = 0
        for cid, _, _, _, _ in completed_consultations:
            if review_count >= 5:
                break
            rid = str(uuid.uuid4())
            rating = random.randint(3, 5)
            await conn.execute(
                '''INSERT INTO reviews (id, consultation_id, rating, comment) 
                   VALUES ($1, $2, $3, $4)''',
                rid, cid, rating, "Great session!"
            )
            review_count += 1
            
        print("Seeding complete.")

    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(seed())
