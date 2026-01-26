class User:
    """
    A class representing a user with an email and a name.

    Attributes:
        email (str): The email address of the user.
        name (str): The name of the user.
    """
    def __init__(self, email: str, name: str):
        """
        Initializes a User object with the given email and name.

        Args:
            email (str): The email address of the user.
            name (str): The name of the user.
        """
        self.email = email
        self.name = name
