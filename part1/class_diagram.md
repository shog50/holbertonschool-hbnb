Explanatory Notes
Entities & Responsibilities
User

Attributes: id, first_name, last_name, email, password, is_admin (for admin checks).

Methods: create(), update(), delete().

Relationships:

Owns 0..* Places (One-to-Many).

Writes 0..* Reviews (One-to-Many).

Place

Attributes: title, description, price, latitude/longitude (location).

Methods: add_amenity(), remove_amenity().

Relationships:

Owned by 1 User (Many-to-One).

Contains 0..* Amenities (Many-to-Many).

Has 0..* Reviews (One-to-Many).

Review

Attributes: comment, rating (validated 1-5).

Methods: validate_rating().

Relationships:

Written by 1 User (Many-to-One).

Belongs to 1 Place (Many-to-One).

Amenity

Attributes: name, description.

Relationships:

Linked to 0..* Places (Many-to-Many).



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
