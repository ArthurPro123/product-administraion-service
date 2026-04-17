
"""Common helper functions for Behave steps"""

from playwright.sync_api import expect
from environment import ID_PREFIX


# ============================================
# HELPER FUNCTIONS
# ============================================

def helper_get_element_id(element_name):
    """'Product Name' → 'product_name'"""
    return ID_PREFIX + element_name.lower().replace(' ', '_')



def helper_get_button_id(button_name):
    """'Create' → 'create-btn'"""
    return button_name.lower().replace(' ', '_') + '-btn'



def helper_get_category_id(category_name):
    """'FOOD' → 2"""
    category_map = {
        'CLOTHS': 1, 'FOOD': 2, 'HOUSEWARES': 3,
        'AUTOMOTIVE': 4, 'TOOLS': 5, 'UNKNOWN': 6
    }
    return category_map.get(category_name.upper(), 6)



def helper_perform_admin_login(context):

    """Perform admin login using UI"""

    # Navigate to home page
    context.page.goto(context.base_url)
    context.page.wait_for_load_state("networkidle")
    
    # Check if already logged in by looking for login button
    login_button = context.page.locator("#login-btn")
    
    if login_button.is_visible():
        # Need to login
        context.page.fill("#login_email", "admin@example.com")
        context.page.fill("#login_password", "admin_pass")
        context.page.click("#login-btn")
        
        # Wait for success message
        expect(context.page.locator("#flash_message")).to_contain_text("Login successful!", timeout=10000)
        print("Admin login completed")
    else:
        # Already logged in
        print("Already logged in as admin")
    
    # Ensure we're on the home page with clean state
    context.page.goto(context.base_url)
    context.page.wait_for_load_state("networkidle")



def helper_ensure_product_exists(context, product_name, category="Tools", price="34.95"):

    """Ensure a product exists using UI (create if not exists)"""

    # First, try to find if product already exists via search
    context.page.fill("#product_name", product_name)
    context.page.click("#search-btn")
    context.page.wait_for_load_state("networkidle")
    
    # Check if product appears in search results
    search_results = context.page.locator("#search_results table tbody tr")
    
    if search_results.count() > 0:
        # Product exists, get its ID
        first_row = search_results.first
        product_id = first_row.locator("td").first.text_content()
        print(f"Product '{product_name}' already exists with ID: {product_id}")
        return product_id
    
    # Product doesn't exist, create it
    context.page.fill("#product_name", product_name)
    context.page.fill("#product_description", f"Test {product_name}")
    context.page.select_option("#product_available", label="True")
    context.page.select_option("#product_category", label=category)
    context.page.fill("#product_price", price)
    context.page.click("#create-btn")
    
    # Wait for creation
    expect(context.page.locator("#flash_message")).to_contain_text("Product created successfully", timeout=10000)
    
    # Get the product ID
    product_id = context.page.input_value("#product_id")
    print(f"Created product '{product_name}' with ID: {product_id}")
    
    # Clear the form for next steps
    context.page.click("#clear-btn")
    
    return product_id
