"""
Test script for database functionality
"""
from database import get_db, execute_query, execute_single_query, execute_write_query, DatabaseError
from werkzeug.security import generate_password_hash
import time

def test_database():
    print("Testing database connection and operations...")
    
    # Generate unique test identifiers
    timestamp = int(time.time())
    test_username = f"test_user_{timestamp}"
    test_org_name = f"Test Organization {timestamp}"
    
    try:
        # Test 1: Database Connection
        print("\n1. Testing database connection...")
        with get_db() as conn:
            print("✓ Database connection successful")
        
        # Test 2: Write Operation (User)
        print("\n2. Testing user creation...")
        user_id = execute_write_query('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (test_username, generate_password_hash('test_password')))
        print(f"✓ Write operation successful - Created user with ID: {user_id}")
        
        # Test 3: Read Operation (Single User)
        print("\n3. Testing single user read...")
        user = execute_single_query('SELECT * FROM users WHERE id = ?', (user_id,))
        print(f"✓ Single read operation successful - Found user: {user['username']}")
        
        # Test 4: Write Operation (Organization)
        print("\n4. Testing organization creation...")
        org_id = execute_write_query('''
            INSERT INTO organizations (name)
            VALUES (?)
        ''', (test_org_name,))
        print(f"✓ Organization created with ID: {org_id}")
        
        # Test 5: Write Operation (User-Organization)
        print("\n5. Testing user-organization relationship...")
        execute_write_query('''
            INSERT INTO user_organizations (user_id, organization_id, role)
            VALUES (?, ?, ?)
        ''', (user_id, org_id, 'admin'))
        print("✓ User-organization relationship created")
        
        # Test 6: Read Operation (Organizations)
        print("\n6. Testing organizations read...")
        orgs = execute_query('''
            SELECT o.*, uo.role
            FROM organizations o
            JOIN user_organizations uo ON o.id = uo.organization_id
            WHERE uo.user_id = ?
        ''', (user_id,))
        print(f"✓ Multiple read operation successful - Found {len(orgs)} organizations")
        
        # Test 7: Write Operation (Inventory)
        print("\n7. Testing inventory creation...")
        item_id = execute_write_query('''
            INSERT INTO inventory (user_id, name, file_type, description)
            VALUES (?, ?, ?, ?)
        ''', (user_id, 'Test Item', 'url', 'Test Description'))
        print(f"✓ Inventory item created with ID: {item_id}")
        
        # Test 8: Write Operation (Announcement)
        print("\n8. Testing announcement creation...")
        announcement_id = execute_write_query('''
            INSERT INTO announcements (organization_id, author_id, title, content)
            VALUES (?, ?, ?, ?)
        ''', (org_id, user_id, 'Test Title', 'Test Content'))
        print(f"✓ Announcement created with ID: {announcement_id}")
        
        # Test 9: Read Operation (Inventory)
        print("\n9. Testing inventory read...")
        items = execute_query('''
            SELECT * FROM inventory WHERE user_id = ?
        ''', (user_id,))
        print(f"✓ Found {len(items)} inventory items")
        
        # Test 10: Read Operation (Announcements)
        print("\n10. Testing announcements read...")
        announcements = execute_query('''
            SELECT * FROM announcements 
            WHERE organization_id = ? AND author_id = ?
        ''', (org_id, user_id))
        print(f"✓ Found {len(announcements)} announcements")
        
        # Test 11: Cleanup
        print("\n11. Testing cleanup...")
        execute_write_query('DELETE FROM announcements WHERE id = ?', (announcement_id,))
        execute_write_query('DELETE FROM inventory WHERE id = ?', (item_id,))
        execute_write_query('DELETE FROM user_organizations WHERE user_id = ?', (user_id,))
        execute_write_query('DELETE FROM organizations WHERE id = ?', (org_id,))
        execute_write_query('DELETE FROM users WHERE id = ?', (user_id,))
        print("✓ Cleanup successful")
        
        print("\n✅ All database tests passed!")
        
    except DatabaseError as e:
        print(f"\n❌ Test failed: {str(e)}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    test_database()
