## Overview
This API powers a web application for DJs, enabling them to create profiles, upload and share music tracks, and manage events. The application supports user authentication using JSON Web Tokens (JWT), ensuring secure access to user-specific data.

Key features include:
- **Profile Management**: Users can create, update, follow and view profiles.
- **Track Uploading**: DJs can upload music tracks, view them, and edit their details.
- **Event Management**: Users can advertise events, specifying date, time, and genre.
- **Permissions**: Data access is restricted, ensuring users can only interact with their own data, such as their profile and tracks.

This API is built using Django and Django REST Framework (DRF), providing a robust, scalable solution for managing user data and interactions.

---

## API Endpoints
The following is a comprehensive list of the available API endpoints in the application. These endpoints allow users to interact with the system, including creating, retrieving, updating, and deleting various resources. The API is designed to be consumed by third-party applications and provides full CRUD (Create, Read, Update, Delete) functionality for all resources.

### `POST /register`
- **Purpose**: Registers a new user in the application.
- **Payload**: Includes user data like email, password, and username.
- **Response**: Returns a success message and HTTP status code 201.

### `POST /login`
- **Purpose**: Authenticates the user and returns a JWT token for secure access to protected routes.
- **Payload**: Includes username and password for login.
- **Response**: Returns an access token and HTTP status code 200.

### `GET /profiles/{id}/`
- **Purpose**: Fetches a user's profile by their ID.
- **Response**: Returns the profile information, including username, bio, image, and any associated tracks or events.

### `POST /tracks/`
- **Purpose**: Allows authenticated users to upload a new track.
- **Payload**: Includes track title, artist, and audio file.
- **Response**: Returns the newly uploaded track's details along with HTTP status code 201.

### `PUT /tracks/{id}/`
- **Purpose**: Allows authenticated users to update the details of their track.
- **Payload**: Includes any fields they wish to update (e.g., title, album cover).
- **Response**: Returns the updated track details.

### `DELETE /tracks/{id}/`
- **Purpose**: Allows users to delete their own tracks.
- **Response**: Returns an HTTP status code 204 (No Content) after deletion.

### `POST /events/`
- **Purpose**: Allows authenticated users to add a new event to the system.
- **Payload**: Includes event details such as name, date, time, and location.
- **Response**: Returns the newly created event's details.

### `GET /events/`
- **Purpose**: Retrieves a list of all events.
- **Response**: Returns a list of events with basic details (e.g., event name, date, location).

### `POST /ratings/`
- **Purpose**: Allows authenticated users to rate a track.
- **Payload**: Includes a rating value (e.g., 1-5 stars) for the track.
- **Response**: Returns the updated track details with the new rating and its average rating.

### `GET /ratings/{track_id}/`
- **Purpose**: Retrieves the ratings for a specific track.
- **Response**: Returns a list of ratings for the track, along with the average rating.

### `POST /comments/`
- **Purpose**: Allows authenticated users to post a comment on a track.
- **Payload**: Includes the comment text and the track ID.
- **Response**: Returns the newly created comment details.

### `GET /comments/{track_id}/`
- **Purpose**: Retrieves all comments for a specific track.
- **Response**: Returns a list of comments for the track.

---

## Database and Model Design

The database schema includes multiple models to represent the key entities of the application. Here's an overview:

### 1. **Profile Model**
   - **Purpose**: Stores information about each user’s profile.
   - **Fields**:
     - `owner`: ForeignKey to the User model (the user who owns this profile).
     - `dj_name`: The DJ's stage name or username.
     - `bio`: A short biography or description of the DJ.
     - `image`: A profile picture for the DJ.
   - **Relationships**: A one-to-one relationship with the User model (through `owner`).
   - **Logic**: Includes methods for retrieving user-specific profile details and updating the profile.

### 2. **Track Model**
   - **Purpose**: Stores information about tracks uploaded by users.
   - **Fields**:
     - `title`: The name of the track.
     - `artist`: The artist or DJ who created the track.
     - `file`: The audio file associated with the track.
     - `owner`: ForeignKey to the Profile model, linking the track to a specific user.
     - `rating`: An average rating for the track.
   - **Relationships**: Each track is associated with one profile, and the track's data can be updated by the track's owner.

### 3. **Event Model**
   - **Purpose**: Stores details about events hosted by users (e.g., DJ gigs, parties).
   - **Fields**:
     - `name`: The name of the event.
     - `date`: The date and time of the event.
     - `location`: The location where the event will take place.
     - `genre`: The genre of music that will be played.
     - `owner`: ForeignKey to the Profile model (the DJ hosting the event).
   - **Relationships**: Each event belongs to one user (Profile).

### 4. **Rating Model**
   - **Purpose**: Represents ratings provided by users for individual tracks.
   - **Fields**:
     - `track`: ForeignKey to the Track model, indicating which track the rating is associated with.
     - `user`: ForeignKey to the User model, identifying the user who gave the rating.
     - `value`: The rating value (typically between 1 and 5 stars).
   - **Relationships**: A many-to-one relationship with the Track model, as multiple ratings can be given to a track.
   - **Logic**: The `Track` model uses these ratings to calculate an average rating for each track.

### 5. **Comment Model**
   - **Purpose**: Stores comments posted by users on tracks.
   - **Fields**:
     - `text`: The content of the comment.
     - `track`: ForeignKey to the Track model, indicating which track the comment relates to.
     - `user`: ForeignKey to the User model, identifying the user who posted the comment.
   - **Relationships**: A one-to-many relationship with the Track model, as multiple comments can be made for a single track.

### 6. **Follower Model**
   - **Purpose**: Represents the relationship between users who follow each other, enabling a social connection between DJs.
   - **Fields**:
     - `follower`: ForeignKey to the User model, representing the user who follows another user.
     - `following`: ForeignKey to the User model, representing the user who is being followed.
   - **Relationships**: 
     - A user (the `follower`) can follow many users (the `following`).
     - A user (the `following`) can be followed by many users (the `follower`).
     - This creates a many-to-many relationship between users.

   - **Logic**:
     - Ensures that a user can follow multiple users and can also be followed by multiple users.
     - A user can’t follow the same user more than once.
     - You could add methods to check if a user is following another user, or retrieve all followers/following for a given user.

---

### Relationships Between Models

- **One-to-Many Relationship**:
  - A **user** can have one **profile**, but a **profile** is owned by only one user. This is a one-to-one relationship, with each user having exactly one profile.
  - A **user** can upload many **tracks**, but each **track** is uploaded by only one user. This is a one-to-many relationship.
  - A **user** can create many **events**, but each **event** is created by only one user. This is also a one-to-many relationship.

- **Many-to-One Relationship**:
  - Many **ratings** can be associated with one **track**. This is a many-to-one relationship, as multiple users can rate the same track.

- **One-to-Many Relationship (Inverse)**:
  - A **track** can have many **comments**, but each **comment** belongs to only one track. This allows for a structured way of displaying user feedback and interactions on individual tracks.

- **Many-to-Many Relationship**:
  - A **user** can follow many other **users** and can be followed by many users. This is implemented via the **Follower** model, which establishes a many-to-many relationship between users, allowing them to follow each other.

---

### Database Structure Considerations for the Follower Model

- **Indexes**:
  - An index would typically be created for the `follower` and `following` fields to improve performance for querying users’ followers and followings.

- **Constraints**:
  - You might want to enforce a constraint that a user cannot follow themselves. This can be handled through validation in the model or within a custom method.

- **Validation**:
  - Ensure that users cannot follow the same person more than once, which may involve checking the existence of the relationship before creating a new entry in the **Follower** model.

---

### Database Structure Considerations

- **Indexes**: 
  - Indexes are applied to frequently queried fields (such as `username` in the `User` model or `track_id` in the `Rating` model) to optimize performance.

- **Constraints**: 
  - Foreign key constraints ensure referential integrity between models, preventing the deletion of records that are still referenced by other records (e.g., a user cannot be deleted if they have an associated profile, track, or event).

- **Validation**:
  - Various fields in the models are validated to ensure data integrity. For example, ratings are validated to be within a predefined range (1-5 stars), and comments have a maximum length to prevent overly long inputs.

---

## CRUD Functionality

### **Create**
- **Profile**: Users can create their own profiles by submitting data such as a stage name, bio, and image.
- **Track**: Users can upload music tracks to the system.
- **Event**: Users can create events by submitting relevant details like event name, date, and genre.
- **Comment**: Users can post comments on tracks.

### **Read**
- **Profiles**: Users can view their own profiles and other public profiles.
- **Tracks**: Users can list all tracks they’ve uploaded and view details of individual tracks.
- **Events**: Users can view a list of all upcoming events.
- **Comments**: Users can view all comments associated with a track.

### **Update**
- **Profile**: Users can update their profile information, including bio and image.
- **Track**: Users can update details of tracks they’ve uploaded (e.g., correcting metadata or updating the audio file).
- **Event**: Users can update event details.
- **Comment**: Users can edit their own comments on tracks.

### **Delete**
- **Track**: Users can delete their own tracks from the system.
- **Event**: Users can delete events they’ve created.
- **Comment**: Users can delete their own comments on tracks.

---

## User Authentication and Authorization

- **JWT Authentication**:
  - Users authenticate by sending their credentials (email and password) to the `/login` endpoint.
  - Upon successful authentication, the API returns a JWT, which users must send in the `Authorization` header for all protected routes.
  
- **Permissions**:
  - **IsOwnerOrReadOnly**: Custom permission class that ensures users can only modify or delete their own data (e.g., profiles and tracks). Users cannot modify other users' profiles or tracks.
  - **Authentication**: The JWT token is required to access any endpoint that interacts with user-specific data (e.g., updating a profile or uploading a track).
  - **Read-only Permissions**: Some endpoints (e.g., viewing tracks and events) may be accessible to any authenticated user.

---

## Testing

### Automated Tests

By implementing a robust suite of automated tests, we ensure that the API maintains high reliability and functionality throughout the development process. These tests help detect issues early, reduce manual testing efforts, and support the deployment of a stable, well-functioning back-end.

Automated testing is an essential part of the development process, ensuring that all the features and functionality of the application work as expected. Below is a breakdown of the automated tests implemented for the various apps in the project:

### Testing Framework
We use **Django's built-in test framework**, which is based on Python's `unittest` module, to create the automated tests. The tests ensure that the back-end API, including the models, views, and permissions, work as expected.

### Testing Coverage

#### **Profile App Tests**
- **Test Profile Creation**:
  - Test the creation of a new user profile to ensure the profile data is saved correctly.
  - Validate the profile fields, including `dj_name`, `bio`, and `image`.
  - Ensure the profile is correctly linked to the user who created it (via the `owner` field).
  
- **Test Profile Updates**:
  - Ensure that the profile data can be updated after it has been created (e.g., changing `dj_name` or `bio`).
  - Verify that only the profile owner can update their profile.

- **Test Profile Deletion**:
  - Ensure that the profile can be deleted, and the related user data is properly removed from the database.

#### **Track App Tests**
- **Test Track Upload**:
  - Test uploading a new track by providing necessary fields like `title`, `artist`, and `file`.
  - Ensure that the track is linked to the correct user (profile) and stored in the database.

- **Test Track Updates**:
  - Test that users can update track details such as `title`, `artist`, and the track file itself.
  - Ensure that updates can only be made by the track owner.

- **Test Track Deletion**:
  - Ensure that users can delete their tracks and that the related track data is removed from the database.

- **Test Track Rating**:
  - Validate that track ratings can be updated and that the average rating is correctly calculated and displayed.
  - Test that only authenticated users can submit ratings.

#### **Event App Tests**
- **Test Event Creation**:
  - Test the creation of a new event with fields like `name`, `date`, `time`, `location`, and `genre`.
  - Ensure that the event is linked to the user who created it (via the `owner` field).

- **Test Event Updates**:
  - Ensure users can update event details, including changing the event name, date, time, or location.

- **Test Event Deletion**:
  - Ensure that users can delete their events and that the event data is correctly removed from the database.

#### **Authentication Tests**
- **Test User Registration**:
  - Test that new users can register by providing their `email`, `username`, and `password`.
  - Validate that the user is correctly created in the database.

- **Test User Login**:
  - Test the login process by ensuring users can authenticate using their credentials (`email` and `password`).
  - Ensure that the JWT token is generated and returned on successful authentication.

- **Test Permissions**:
  - Ensure that users can only access their own data (e.g., their profile and tracks).
  - Test the behavior when attempting to access or modify resources owned by other users (should be denied with appropriate permissions).

### Test Execution

- **Running Tests**:
  - All automated tests can be executed using the `python manage.py test` command.
  - The tests are run automatically in a local development environment and on the CI/CD pipeline (if set up).

- **Test Results**:
  - After running the tests, the output will indicate whether each test passed or failed. In case of failure, detailed error messages will help pinpoint the issue.

### CI/CD Integration (Optional)
If applicable, describe how the automated tests are integrated into the CI/CD pipeline for continuous testing on every push or pull request:
- Example: "The tests are automatically run on each push to GitHub, ensuring that code changes do not break any functionality."

---

## Test Coverage and Code Quality

- **Code Coverage**:
  - All critical functionality, including model methods, views, and authentication processes, is covered by automated tests.
  - Use tools like `coverage.py` to measure the test coverage of the codebase, ensuring that all critical parts of the application are tested.

- **Code Quality**:
  - Tests are written following PEP8 guidelines, ensuring readability and consistency across the codebase.
  - Test names are descriptive and follow a consistent naming convention for easy identification.

---


### Manual Testing

In addition to the automated tests, manual testing is conducted to ensure the application functions correctly from a user perspective. This includes checking the user interface, ensuring that data is presented correctly, and manually testing edge cases that may not be easily automated.

- **Profile Endpoints**:
  - Test the `POST /register` and `POST /login` endpoints with valid and invalid data to ensure proper authentication.
  - Test the `GET /profiles/{id}/` to check if profile data is retrieved correctly.
  
- **Track Endpoints**:
  - Test the `POST /tracks/` with a valid track file and ensure the track is saved to the database.
  - Test the `PUT /tracks/{id}/` to update the track's metadata.
  - Test the `DELETE /tracks/{id}/` to ensure only the track owner can delete a track.

- **Event Endpoints**:
  - Test the `POST /events/` with valid event data.
  - Test the `GET /events/` to list events and ensure data integrity.

### Test Coverage
- **Unit Tests**: If you have any unit tests or functional tests, include them in the README and describe what parts of the application they cover.
- **Testing Strategy**: Outline the testing methods used (e.g., postman, unit tests with Django’s test framework).

---

## Deployment Instructions

To deploy the API to **Heroku** (or another platform like **AWS** or **DigitalOcean**), follow these steps:

1. **Set Up Your Heroku App**:
   - Run `heroku create` to create a new app.
   - Push the code to Heroku: `git push heroku master`.

2. **Set Up Environment Variables**:
   - Set secret keys and configurations in Heroku using `heroku config:set` commands for variables like:
     - `SECRET_KEY`
     - `JWT_SECRET_KEY`
     - Database configurations
  
3. **Migrate the Database**:
   - Run the migrations on Heroku: `heroku run python manage.py migrate`.

4. **Start the Application**:
   - If necessary, scale the application using `heroku ps:scale web=1`.

---

## Security Considerations

- **Environment Variables**: All sensitive data (API keys, passwords, JWT secrets) are stored as environment variables, ensuring that they are not exposed in the codebase.
- **Secure Authentication**: JWT tokens are used for user authentication. These tokens are stored securely and transmitted over HTTPS.
- **Debug Mode**: Ensure `DEBUG = False` in the production environment to avoid exposing sensitive error information.

---

## Git & GitHub Usage

- **Version Control**: All changes are tracked using Git and pushed to GitHub. Features were developed in separate branches, and GitHub Issues were used to manage tasks and bugs.
  - Example commit message: "Implemented JWT authentication for login endpoint."
- **Commit Messages**: Keep messages clear and descriptive, following best practices (e.g., “Refactored track upload endpoint”).
- **GitHub Projects**: If applicable, mention using GitHub Projects for task management and agile workflows.

---

## Front-End Integration

- **Front-End Communication**: The front-end application communicates with the back-end API to fetch and manipulate user data. For example, users can view their profile and upload tracks via the React app, which sends requests to the back-end API.

- **CORS**: Ensure that Cross-Origin Resource Sharing (CORS) is properly configured to allow the front-end app to interact with the API.

