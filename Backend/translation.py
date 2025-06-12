import json

class Translation:
    """
    Translates data for backend and frontend usage
    """ 

    @staticmethod
    
    def json_to_dict(json_string: str) -> dict:
        """
        Converts a JSON-formatted string into a Python dictionary.

        Args:
            json_string (str): A string in valid JSON format.

        Returns:
            dict: The corresponding Python dictionary.
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
