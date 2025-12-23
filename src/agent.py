import sys
import os
import json

# Ensure we can find the src module regardless of where this script is run
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src.logic import PolicyEngine

AGENT_NAME = "SchemeSetu_Agent_v1"

class SchemeSetuAgent:
    """
    Main agent class that handles incoming JSON requests and routes them 
    to the appropriate logic handler (PolicyEngine).
    """
    def __init__(self):
        # Initialize the logic engine with the path to the database
        data_path = os.path.join(parent_dir, 'data', 'schemes.json')
        self.brain = PolicyEngine(data_path)

    def listen(self, message_json):
        """
        Processes a JSON string request.
        Supports: 'check_eligibility' and 'learn_new_scheme'.
        """
        try:
            request_data = json.loads(message_json)
            req_type = request_data.get('request_type', 'check_eligibility')

            # Route: Check Eligibility
            if req_type == 'check_eligibility':
                user_age = request_data.get('age')
                user_income = request_data.get('income')
                user_caste = request_data.get('caste', 'General')
                
                # Validation: Default to 0 if fields are missing to avoid NoneType errors
                if user_age is None: user_age = 0
                if user_income is None: user_income = 0

                results = self.brain.check_eligibility(user_age, user_income, user_caste)
                
                return json.dumps({
                    "sender": AGENT_NAME,
                    "status": "success",
                    "data": results
                }, indent=2)

            # Route: Admin/Teacher Mode (Add new scheme)
            elif req_type == 'learn_new_scheme':
                new_scheme = request_data.get('scheme_data')
                if new_scheme:
                    new_id = self.brain.add_scheme(new_scheme)
                    return json.dumps({
                        "sender": AGENT_NAME,
                        "status": "success",
                        "message": f"New scheme learned successfully. ID: {new_id}"
                    }, indent=2)
                else:
                    return json.dumps({"status": "error", "message": "No scheme_data provided"})

            else:
                return json.dumps({"status": "error", "message": f"Unknown request type: {req_type}"})

        except Exception as e:
            # Log error to console for debugging
            print(f"[Agent Error] {str(e)}")
            return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    # Test execution
    try:
        agent = SchemeSetuAgent()
        print(f"✅ {AGENT_NAME} initialized and ready.")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")