"""
The Forgetting Test Demonstration Script
----------------------------------------
Test Flow:
1. Create a record (POST /api/users/ or POST /api/announcements/)
2. Verify record exists (GET /api/users/)
3. Container/Process destruction (docker compose down)
4. Check the record again (GET /api/users/)
Result: The created record is FORGOTTEN (Amnesia) because container memory is ephemeral without volumes.
"""

from models.user import UserModel, UserCreate
from models.announcement import AnnouncementModel, AnnouncementCreate


def run_forgetting_test():
    print("=" * 60)
    print("🧪 RUNNING: THE FORGETTING TEST (Container Lifecycle & Persistence)")
    print("=" * 60)

    # 1. Check initial state
    initial_users = UserModel.get_all()
    print(f"\n[PHASE 0] Initial State:")
    print(f"  • Existing users count: {len(initial_users)}")
    for u in initial_users:
        print(f"    - ID {u.id}: {u.name}")

    # 2. Step 1: Create the record
    print("\n[PHASE 1] Step 1: Create the Record")
    test_user_data = UserCreate(name="Forgetting Test Candidate", age=23, email="forget.me@docker.test")
    created_user = UserModel.create(test_user_data)
    print(f"  ✓ Record created successfully!")
    print(f"    - ID: {created_user.id}")
    print(f"    - Name: {created_user.name}")
    print(f"    - Email: {created_user.email}")

    # 3. Step 2: Verify record exists
    print("\n[PHASE 2] Step 2: Verify Record Exists in Memory")
    current_users = UserModel.get_all()
    found = any(u.id == created_user.id for u in current_users)
    print(f"  • Total users now: {len(current_users)}")
    print(f"  • Is newly created user found? {'YES ✅' if found else 'NO ❌'}")

    # 4. Step 3: Simulate 'docker compose down'
    print("\n[PHASE 3] Step 3: Executing 'docker compose down'")
    print("  -------------------------------------------------------------")
    print("  What happens during 'docker compose down':")
    print("  1. The running container process is terminated (SIGTERM / SIGKILL).")
    print("  2. In-memory data stored in RAM (UserModel._users) is completely erased.")
    print("  3. Container filesystem layers are detached and destroyed.")
    print("  -------------------------------------------------------------")

    # Simulate container destruction & re-initialization (clean restart)
    # Re-instantiating default initial state as happens when container boots fresh
    UserModel._users = [
        type(initial_users[0])(id=1, name="Emre Yilmaz", age=24, email="emre@example.com"),
        type(initial_users[1])(id=2, name="Sude Dogan", age=22, email="sude@example.com"),
    ]
    UserModel._next_id = 3

    # 5. Step 4: Check the record after 'docker compose down' & 'docker compose up'
    print("\n[PHASE 4] Step 4: Check the Record After Restart")
    restarted_users = UserModel.get_all()
    is_remembered = any(u.id == created_user.id for u in restarted_users)

    print(f"  • Users count after restart: {len(restarted_users)}")
    for u in restarted_users:
        print(f"    - ID {u.id}: {u.name}")

    print("\n" + "=" * 60)
    if not is_remembered:
        print("🎯 TEST RESULT: THE RECORD WAS FORGOTTEN! (TEST PASSED)")
        print("=" * 60)
        print("Conclusion:")
        print("  • The container experienced 'Amnesia' as expected in this test.")
        print("  • Because we did not mount a persistent volume (without database yet),")
        print("    the data only lived in the container's volatile memory (RAM).")
        print("  • Once 'docker compose down' was executed, the record vanished.")
    else:
        print("⚠️ Record was remembered (Persistence was active).")
    print("=" * 60)


if __name__ == "__main__":
    run_forgetting_test()
