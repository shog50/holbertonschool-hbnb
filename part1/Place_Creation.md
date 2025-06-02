# Explanatory Notes
Purpose
Depicts the flow for creating a new place, including:

Input validation (price, title).

Authorization checks (owner existence).

Success/error responses.

Key Steps
User Request:

Submits title, price, and owner_id to PlaceAPI.

Validation:

Business Logic checks if price is valid (e.g., positive number).

Invalid: Returns 400 Bad Request with error details.

Owner Verification:

Database checks if owner_id exists.

Invalid: Returns 404 Not Found if owner doesn’t exist.

Place Creation:

Valid data is saved to the database.

Success: Returns 201 Created with the new place_id and title.


# Place Creation
```mermaid
---
config:
  theme: forest
  look: handDrawn
---
sequenceDiagram
    participant User
    participant API as PlaceAPI
    participant BusinessLogic as Place
    participant Database as PlaceRepository
    User->>API: Create place (title, price, owner_id)
    API->>BusinessLogic: Validate + auth
    alt Invalid Data
        BusinessLogic-->>API: Error("Invalid price")
        API-->>User: 400 Bad Request
    else Valid
        BusinessLogic->>Database: Verify owner_id
        Database-->>BusinessLogic: Owner data
        alt Owner Invalid
            BusinessLogic-->>API: Error("Owner not found")
            API-->>User: 404 Not Found
        else Valid
            BusinessLogic->>Database: Save place
            Database-->>BusinessLogic: place_id
            BusinessLogic-->>API: Success
            API-->>User: 201 Created (id, title)
        end
    end
