"""
Test script to verify ticket status update functionality
Run this after starting the backend to test the fixes
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000/api"
ADMIN_EMAIL = "admin@nexora.ai"
ADMIN_PASSWORD = "admin123"

def test_status_update():
    print("=" * 60)
    print("Testing Ticket Status Update Functionality")
    print("=" * 60)
    
    # Step 1: Login as admin
    print("\n1. Logging in as admin...")
    login_response = requests.post(f"{BASE_URL}/login", json={
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return
    
    token = login_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")
    
    # Step 2: Get all tickets
    print("\n2. Fetching all tickets...")
    tickets_response = requests.get(f"{BASE_URL}/admin/tickets", headers=headers)
    
    if tickets_response.status_code != 200:
        print(f"❌ Failed to fetch tickets: {tickets_response.text}")
        return
    
    tickets = tickets_response.json()["tickets"]
    print(f"✅ Found {len(tickets)} tickets")
    
    if len(tickets) == 0:
        print("⚠️  No tickets found. Please create a ticket first.")
        return
    
    # Step 3: Get analytics before update
    print("\n3. Getting analytics before status update...")
    analytics_before = requests.get(f"{BASE_URL}/admin/advanced-analytics", headers=headers)
    
    if analytics_before.status_code != 200:
        print(f"❌ Failed to fetch analytics: {analytics_before.text}")
        return
    
    resolved_before = analytics_before.json()["resolved_tickets"]
    print(f"✅ Resolved tickets before: {resolved_before}")
    
    # Step 4: Find a ticket that is not resolved
    test_ticket = None
    for ticket in tickets:
        if ticket["status"] != "resolved" and ticket["status"] != "closed":
            test_ticket = ticket
            break
    
    if not test_ticket:
        print("⚠️  No open tickets found. All tickets are already resolved.")
        # Try to find a resolved ticket to test reverting
        for ticket in tickets:
            if ticket["status"] == "resolved":
                test_ticket = ticket
                break
    
    if not test_ticket:
        print("❌ No suitable test ticket found")
        return
    
    print(f"\n4. Testing with ticket: #{test_ticket['id'][:8]}")
    print(f"   Current status: {test_ticket['status']}")
    print(f"   Current resolved_at: {test_ticket.get('resolved_at', 'None')}")
    
    # Step 5: Update ticket status to resolved
    new_status = "resolved" if test_ticket["status"] != "resolved" else "open"
    print(f"\n5. Updating ticket status to '{new_status}'...")
    
    update_response = requests.put(f"{BASE_URL}/update-ticket", 
        headers={**headers, "Content-Type": "application/json"},
        json={
            "ticket_id": test_ticket["id"],
            "status": new_status
        }
    )
    
    if update_response.status_code != 200:
        print(f"❌ Failed to update ticket: {update_response.text}")
        return
    
    updated_ticket = update_response.json()["ticket"]
    print(f"✅ Ticket updated successfully")
    print(f"   New status: {updated_ticket['status']}")
    print(f"   New resolved_at: {updated_ticket.get('resolved_at', 'None')}")
    
    # Step 6: Verify resolved_at timestamp
    if new_status == "resolved":
        if updated_ticket.get("resolved_at"):
            print("✅ resolved_at timestamp was set correctly")
        else:
            print("❌ resolved_at timestamp was NOT set (BUG!)")
    else:
        if not updated_ticket.get("resolved_at"):
            print("✅ resolved_at timestamp was cleared correctly")
        else:
            print("⚠️  resolved_at timestamp still exists")
    
    # Step 7: Get analytics after update
    print("\n6. Getting analytics after status update...")
    analytics_after = requests.get(f"{BASE_URL}/admin/advanced-analytics", headers=headers)
    
    if analytics_after.status_code != 200:
        print(f"❌ Failed to fetch analytics: {analytics_after.text}")
        return
    
    resolved_after = analytics_after.json()["resolved_tickets"]
    print(f"✅ Resolved tickets after: {resolved_after}")
    
    # Step 8: Verify count changed
    expected_change = 1 if new_status == "resolved" else -1
    actual_change = resolved_after - resolved_before
    
    if actual_change == expected_change:
        print(f"✅ Resolved ticket count changed correctly ({resolved_before} → {resolved_after})")
    else:
        print(f"❌ Resolved ticket count did NOT change correctly")
        print(f"   Expected change: {expected_change}, Actual change: {actual_change}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_status_update()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
