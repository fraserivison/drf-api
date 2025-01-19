# Wave App API Backend

## Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
  - [Frameworks and Libraries](#frameworks-and-libraries)
  - [Database](#database)
- [Installation Instructions](#installation-instructions)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Database and Model Design](#database-and-model-design)
- [CRUD Functionality](#crud-functionality)
- [User Authentication and Authorisation](#user-authentication-and-authorisation)
- [Testing](#testing)
  - [Automated Testing](#automated-testing)
  - [Manual Testing](#manual-testing)
- [Deployment Instructions](#deployment-instructions)
- [Security Considerations](#security-considerations)
- [Git & GitHub Usage](#git-and-github-usage)
- [Front-End Integration](#front-end-integration)

[Back to top](#table-of-contents)

## Overview
This API powers a web application for DJs, enabling them to create profiles, upload and share music tracks, and manage events. The application supports user authentication using JSON Web Tokens (JWT), ensuring secure access to user-specific data.

## Technologies Used

### Frameworks and Libraries:
- **Django**: The web framework used to build the backend.
- **Django REST Framework (DRF)**: A toolkit for building APIs in Django.
- **PostgreSQL**: The relational database system used for data storage.
- **JWT (JSON Web Token)**: For handling secure user authentication.
- **Cloudinary**: Used for storing and managing media files such as music tracks and cover art.

### Database:
- **PostgreSQL** is used as the database system for this project, providing a robust and scalable relational database to store user data, tracks, ratings, and events. The database schema includes custom models for users, tracks, ratings, and events, ensuring a structured and organized data flow.

## Installation Instructions

1. Install the required dependencies: pip install -r requirements.txt
2. If you are using PostgreSQL, ensure that you have created a database: createdb your_database_name
3. Apply Migrations: python manage.py migrate
4. If you're not using the default SQLite database, you'll need to configure your database connection settings. In your settings.py, ensure that the DATABASES configuration is set up with the correct credentials. You can also pass the database URL as an environment variable:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

5. Create a Superuser: python manage.py createsuperuser
6. Once you've completed the database setup, you can start the development server using: python manage.py runserver
7. Make sure to configure the following environment variables for the project to run correctly
- SECRET_KEY: Generate a Django secret key (can use Django Secret Key Generator) and add it as an environment variable.
- DATABASE_URL: Provide the database URL for different environments (local, production).
- CLOUDINARY_URL: Set to your Cloudinary URL for media storage (only if using Cloudinary for images/media).
- DEBUG: In production, ensure that DEBUG is set to False to avoid exposing sensitive information.
- ALLOWED_HOSTS: Add the domains or IP addresses that can access the API (e.g., ALLOWED_HOSTS = ['your-domain.com']).
- CLIENT_ORIGIN: Specify the URL of the front-end application that will be making requests to this API (e.g., http://localhost:3000).
- CLIENT_ORIGIN_DEV: For local development, specify the address of the local server used to preview and test the UI during front-end development (e.g., http://127.0.0.1:3000).
- Ensure that your .env file is not tracked by git by adding it to .gitignore.

## Features

Key features include:
- **Track Uploading**: DJs can upload music tracks, view them, and edit their details.
- **Event Management**: Users can advertise events, specifying date, time, and genre.
- **Permissions**: Data access is restricted, ensuring users can only interact with their own data, such as their profile and tracks.

- **Profile Management**: Users can create, update, follow and view profiles.


---

## API Endpoints
The following is a comprehensive list of the available API endpoints in the application. These endpoints allow users to interact with the system, including creating, retrieving, updating, and deleting various resources. The API is designed to be consumed by third-party applications and provides full CRUD (Create, Read, Update, Delete) functionality for all resources.

### `POST /register`
- **Purpose**: Registers a new user in the application.
- **Payload**: Includes user data like email, password, and owner.
- **Response**: Returns a success message and HTTP status code 201.

### `POST /login`
- **Purpose**: Authenticates the user and returns a JWT token for secure access to protected routes.
- **Payload**: Includes owner and password for login.
- **Response**: Returns an access token and HTTP status code 200.

### `GET /profiles/{id}/`
- **Purpose**: Fetches a user's profile by their ID.
- **Response**: Returns the profile information, including owner, bio, image, and any associated tracks or events.

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
     - `dj_name`: The DJ's stage name or owner.
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

## User Authentication and Authorisation

- **JWT Authentication**:
  - Users authenticate by sending their credentials (email and password) to the `/login` endpoint.
  - Upon successful authentication, the API returns a JWT, which users must send in the `Authorization` header for all protected routes.
  
- **Permissions**:
  - **IsownerOrReadOnly**: Custom permission class that ensures users can only modify or delete their own data (e.g., profiles and tracks). Users cannot modify other users' profiles or tracks.
  - **Authentication**: The JWT token is required to access any endpoint that interacts with user-specific data (e.g., updating a profile or uploading a track).
  - **Read-only Permissions**: Some endpoints (e.g., viewing tracks and events) may be accessible to any authenticated user.

---

## Testing

### Automated Testing

By implementing a robust suite of automated tests, we ensure that the API maintains high reliability and functionality throughout the development process. These tests help detect issues early, reduce manual testing efforts, and support the deployment of a stable, well-functioning back-end.

Automated testing is an essential part of the development process, ensuring that all the features and functionality of the application work as expected. Below is a breakdown of the automated tests implemented for the various apps in the project:

#### **Testing Framework**
**Django's built-in test framework** was used, which is based on Python's `unittest` module, to create the automated tests. The tests ensure that the back-end API, including the models, views, and permissions, work as expected.

##### **Profile App Tests**
- **Test Profile Creation**:
  - Test the creation of a new user profile to ensure the profile data is saved correctly.
  - Validate the profile fields, including `dj_name`, `bio`, and `image`.
  - Ensure the profile is correctly linked to the user who created it (via the `owner` field).
  
- **Test Profile Updates**:
  - Ensure that the profile data can be updated after it has been created (e.g., changing `dj_name` or `bio`).
  - Verify that only the profile owner can update their profile.

- **Test Profile Deletion**:
  - Ensure that the profile can be deleted, and the related user data is properly removed from the database.

##### **Track App Tests**
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

##### **Event App Tests**
- **Test Event Creation**:
  - Test the creation of a new event with fields like `name`, `date`, `time`, `location`, and `genre`.
  - Ensure that the event is linked to the user who created it (via the `owner` field).

- **Test Event Updates**:
  - Ensure users can update event details, including changing the event name, date, time, or location.

- **Test Event Deletion**:
  - Ensure that users can delete their events and that the event data is correctly removed from the database.

##### **Authentication Tests**
- **Test User Registration**:
  - Test that new users can register by providing their `email`, `owner`, and `password`.
  - Validate that the user is correctly created in the database.

- **Test User Login**:
  - Test the login process by ensuring users can authenticate using their credentials (`email` and `password`).
  - Ensure that the JWT token is generated and returned on successful authentication.

- **Test Permissions**:
  - Ensure that users can only access their own data (e.g., their profile and tracks).
  - Test the behavior when attempting to access or modify resources owned by other users (should be denied with appropriate permissions).

##### **Comments App Tests**
- **Test Comment Creation**:
  - Ensure users can create comments on tracks, with validation for required fields like the comment text.
  - Ensure the comment is correctly linked to the track and the user (via the `track` and `user` fields).

- **Test Comment Updates**:
  - Test that users can update their comments, ensuring only the comment's creator can make changes.

- **Test Comment Deletion**:
  - Ensure that users can delete their comments, and the related comment data is removed from the database.

##### **Ratings App Tests**
- **Test Rating Creation**:
  - Ensure users can create ratings for tracks, with validation for required fields like the rating value.
  - Ensure that the rating is linked to the correct track and user.

- **Test Rating Updates**:
  - Test that users can update their ratings for a track and that the `average_rating` field is updated accordingly.

- **Test Rating Deletion**:
  - Ensure users can delete their ratings, and the track's rating is updated accordingly.

##### **Followers App Tests**
- **Test Follow User**:
  - Test that a user can follow another user and that the `followers` field is correctly updated.
  - Ensure that the follow action cannot be performed by the user on themselves.

- **Test Unfollow User**:
  - Ensure users can unfollow other users and that the `followers` field is updated accordingly.

- **Test Follow Count**:
  - Verify that the number of followers and following is correctly updated when users follow or unfollow each other.

#### **Key Tests Written**
- **Profile Creation on User Registration**: 
  - When a user is created, a corresponding `Profile` object is automatically created for that user. 
  - This test verifies that a `Profile` is created when a new `User` is registered, ensuring the one-to-one relationship between `User` and `Profile` works as expected.

- **Track Creation and ownership**:
  - When a `Track` is created, it must be linked to a `Profile` (the owner).
  - The test ensures that a newly created `Track` is associated with the correct `Profile` and that the `owner` field is populated correctly.

- **Track Rating Updates**:
  - The `Track` model includes logic for updating the average rating and rating count. 
  - This test checks if the `average_rating` and `ratings_count` fields are updated correctly when a new rating is added.

- **Track File Validation**:
  - To ensure that only valid audio files (within a 100MB size limit) can be uploaded, tests are in place to validate the file size and format during track creation. 
  - This test ensures that an error message is returned if the uploaded file exceeds the size limit or is in an unsupported format.

- **Profile Serializer**:
  - The `ProfileSerializer` was tested to ensure that it correctly returns the DJ's name and other details in the expected format when serializing profile data.

- **API Endpoint Testing**:
  - **Track List Endpoint**: Verifies that the `TrackList` API returns the correct list of tracks, with the correct filtering, search, and ordering functionality.
  - **Track Detail Endpoint**: Tests the `TrackDetail` API to ensure that the detailed information for a track, including the owner's name (via the `Profile` model), is correctly returned.

#### **Running the Tests**

To run the tests for this project, use the following command in the terminal: **python manage.py test**

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
  - Test the `PUT /events/{id}/` to ensure users can update event details.

- **Comment Endpoints**:
  - Test the `POST /comments/` to ensure users can comment on tracks.
  - Test the `GET /comments/{id}/` to verify that comments can be retrieved.
  - Test the `PUT /comments/{id}/` to ensure users can update their own comments.
  - Test the `DELETE /comments/{id}/` to ensure users can delete their own comments.

- **Rating Endpoints**:
  - Test the `POST /ratings/` to ensure users can rate tracks.
  - Test the `GET /ratings/{id}/` to verify that ratings are correctly linked to tracks.
  - Test the `PUT /ratings/{id}/` to ensure users can update their ratings (since deletion is not allowed).
  - Test the `DELETE /ratings/{id}/` to ensure users can delete a rating.


- **Followers Endpoints**:
  - Test the `POST /follow/` to ensure users can follow others.
  - Test the `GET /followers/{id}/` to retrieve the list of followers for a user.
  - Test the `DELETE /follow/{id}/` to ensure users can unfollow others.

### Test Coverage
- **Unit Tests**: If you have any unit tests or functional tests, include them in the README and describe what parts of the application they cover.
- **Testing Strategy**: Outline the testing methods used (e.g., postman, unit tests with Django’s test framework).

---

## Deployment Instructions

The site was deployed to Heroku. The steps to deploy are as follows:

1. Navigate to [Heroku](https://www.heroku.com) and create an account if you don't have one.
2. Click the **New** button in the top right corner.
3. Select **Create New App**.
4. Enter a name for your app.
5. Select a region and click **Create App**.
6. Go to the **Settings** tab and click **Reveal Config Vars**.
7. Add the following config vars:
   - `SECRET_KEY`: (Your secret key)
   - `DATABASE_URL`: (This should already exist)
   - `ALLOWED_HOST`: (Set this to your allowed host domain)
   - `CLIENT_ORIGIN`: URL for the client front-end React application that will be making requests to these APIs
   - `CLIENT_ORIGIN_DEV`: Address of the local server used to preview and test the UI during development of the front-end client application
   - `CLOUDINARY_URL`: Set to your Cloudinary URL
   - `DISABLE_COLLECTSTATIC`: `1`
8. Click the **Deploy** tab.
9. Scroll down to **Connect to GitHub** and sign in/authorize when prompted.
10. In the search box, find the repository you want to deploy and click **Connect**.
11. Scroll down to **Manual Deploy** and choose the **main** branch to deploy your app.

Once the deployment process is complete, the app should be live on Heroku.

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


[Back to top](#table-of-contents)