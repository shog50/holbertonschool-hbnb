# Explanatory Notes

Purpose
Illustrates the end-to-end flow for submitting a review, including:

Validation of the rating.

Checks for place existence and ownership conflicts.

Success/error responses.

Key Steps
User Request:

Submits place_id and rating (1-5) to ReviewAPI.

Validation:

Business Logic verifies the rating is between 1-5.

Invalid: Returns 400 Bad Request with an error message.

Place Verification:

Database fetches the place and its owner.

Place Missing: Returns 404 Not Found.

Author is Owner: Blocks self-reviews with 403 Forbidden.

Review Creation:

Valid reviews are saved to the database.

Success: Returns 201 Created with the review_id and rating.

# Review Submission
```mermaid
---
config:
  theme: forest
  look: handDrawn
---
sequenceDiagram
    participant User
    participant API as ReviewAPI
    participant BusinessLogic as Review
    participant Database as ReviewRepository
    User->>API: Submit review (place_id, rating)
    API->>BusinessLogic: Validate
    alt Invalid Rating
        BusinessLogic-->>API: Error("Rating 1-5")
        API-->>User: 400 Bad Request
    else Valid
        BusinessLogic->>Database: Get place + owner
        Database-->>BusinessLogic: Place data
        alt Place Missing
            BusinessLogic-->>API: Error("Place not found")
            API-->>User: 404 Not Found
        else Author is Owner
            BusinessLogic-->>API: Error("No self-reviews")
            API-->>User: 403 Forbidden
        else Valid
            BusinessLogic->>Database: Save review
            Database-->>BusinessLogic: review_id
            BusinessLogic-->>API: Success
            API-->>User: 201 Created (id, rating)
        end
    end
