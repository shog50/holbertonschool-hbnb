#Explanatory Notes

Explanatory Notes:

Purpose: Depicts the user registration process, including validation, conflict checks, and successful creation.

Key Steps:

User submits registration data.

Business logic validates email/password format (returns 400 if invalid).

Database checks for existing email (returns 409 if conflict).

Password is hashed, and user is saved (returns 201 on success).

# User Registration:
sequenceDiagram
    participant User
    participant API as UserAPI
    participant BusinessLogic as User
    participant Database as UserRepository
    User->>API: Register (name, email, password)
    API->>BusinessLogic: Validate format
    alt Invalid Email/Password
        BusinessLogic-->>API: Error("Invalid format")
        API-->>User: 400 Bad Request
    else Valid
        BusinessLogic->>Database: Check email exists
        Database-->>BusinessLogic: Result
        alt Email Exists
            BusinessLogic-->>API: Error("Email taken")
            API-->>User: 409 Conflict
        else New User
            BusinessLogic->>BusinessLogic: hash_password()
            BusinessLogic->>Database: Save user
            Database-->>BusinessLogic: user_id
            BusinessLogic-->>API: Success
            API-->>User: 201 Created (id, email)
        end
    end
