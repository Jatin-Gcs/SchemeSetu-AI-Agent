import json
import os

class PolicyEngine:
    """
    Core logic engine responsible for managing scheme data and 
    evaluating user eligibility against defined rules.
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.schemes = self.load_schemes()

    def load_schemes(self):
        """
        Loads scheme data from the local JSON storage.
        Returns an empty list if file doesn't exist or is corrupted.
        """
        if not os.path.exists(self.data_path):
            return []

        try:
            with open(self.data_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return empty list on error to prevent crash
            return []

    def save_schemes(self):
        """Persists the current list of schemes to the JSON file."""
        try:
            with open(self.data_path, 'w', encoding='utf-8') as file:
                json.dump(self.schemes, file, indent=2)
        except IOError as e:
            print(f"[Error] Failed to save schemes: {e}")

    def add_scheme(self, new_scheme_data):
        """
        Adds a new scheme to the database.
        Automatically generates a sequential ID (e.g., SCH001).
        """
        # Generate ID based on current count
        next_id = len(self.schemes) + 1
        scheme_id = f"SCH{next_id:03d}"
        
        new_scheme_data['id'] = scheme_id
        
        self.schemes.append(new_scheme_data)
        self.save_schemes()
        
        return scheme_id

    def check_eligibility(self, user_age, user_income, user_category):
        """
        Filters the available schemes based on the user's demographic data.
        """
        eligible_schemes = []
        
        for scheme in self.schemes:
            rules = scheme.get('rules', {})
            
            # 1. Check Age Limits
            min_age = rules.get('min_age', 0)
            max_age = rules.get('max_age', 100)
            
            if not (min_age <= user_age <= max_age):
                continue 
            
            # 2. Check Income Limits
            # Default to infinity if no limit is specified
            max_income = rules.get('max_income', float('inf'))
            
            if user_income > max_income:
                continue 
            
            # 3. Check Category/Caste Eligibility
            allowed_categories = rules.get('category', [])
            
            # If specific categories are listed, user must match one
            if allowed_categories and user_category not in allowed_categories:
                continue
            
            # If all checks pass, add to results
            eligible_schemes.append(scheme)
            
        return eligible_schemes