# Detailed Class Diagram (Business Logic Layer)

```mermaid
classDiagram
    class User {
        +String id (UUID4)
        +String first_name
        +String last_name
        +String email
        +String password
        +Bool is_admin
        +DateTime created_at
        +DateTime updated_at
        +create() User
        +update() Bool
        +delete() Bool
    }

    class Place {
        +String id (UUID4)
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +User owner
        +List~Amenity~ amenities
        +DateTime created_at
        +DateTime updated_at
        +add_amenity(Amenity) Bool
        +remove_amenity(Amenity) Bool
    }

    class Review {
        +String id (UUID4)
        +String comment
        +Int rating (1-5)
        +User author
        +Place place
        +DateTime created_at
        +DateTime updated_at
        +validate_rating() Bool
    }

    class Amenity {
        +String id (UUID4)
        +String name
        +String description
        +DateTime created_at
        +DateTime updated_at
    }

    User "1" -- "0..*" Place : Owns
    User "1" -- "0..*" Review : Writes
    Place "1" -- "0..*" Review : Has
    Place "0..*" -- "0..*" Amenity : Contains
