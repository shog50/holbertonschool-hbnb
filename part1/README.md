HBnB Evolution Clean Architecture Backend

A modular backend design for a property listing and booking platform, similar to AirBnB. This architecture separates concerns into three layers: Presentation, Business Logic, and Persistence. The system supports operations such as user registration, place creation, review submission, and amenity management.
- High-Level Architecture
  Layer Responsibilities
  1. Presentation Layer (API): Handles HTTP requests/responses. Forwards calls to the business logic.
E.g., POST /users → User.create().

  2. Business Logic Layer (Models): Core domain logic: validation, transformations, and decision-making.

  3. Persistence Layer (Repositories): Handles database operations. Acts as an interface to the storage layer.
- Business Logic Layer
- Sequence Diagrams
1. 🧾 User Registration
2. 🏠 Place Creation
3. 🧾 Review Submission
4. 🔍 Fetching Places (Filter by Price)
   
- Key Features
1. Clean architecture with clear separation of concerns
2. Input validation, error handling, and ownership verification
3. Modular design (easily testable and extensible)
4. UUID identifiers and timestamp tracking for all entities
5. Supports CRUD operations for Users, Places, Reviews, and Amenities
