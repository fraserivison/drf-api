# Backend README for Social Media App

## Overview

This project is a social media platform built for DJs to upload, share, and discover music. The backend is developed using Django and Django REST framework (DRF), and it provides an API for communication with the front end, allowing for various functionalities such as user authentication, music upload, track rating, event management, and user interaction features like following and commenting.

### Key Features of the Backend:
- **User Authentication**: Using `django-allauth` for user login, registration, and token-based authentication (JWT).
- **Music Upload and Sharing**: Users can upload tracks and have them displayed in their profile and the discovery feed.
- **Track Rating**: Users can rate tracks on a 1-5 star scale, with average ratings displayed.
- **Event Management**: Users can create and share events with details such as date, location, and genre.
- **CRUD Operations**: For tracks, events, user profiles, and comments.
- **Security**: User data is secured, and API keys and passwords are stored in environment variables.

---

## App Structure

### Models

1. **Profile Model**: Stores user-specific information like bio, profile picture, and links to events and tracks.
2. **Track Model**: Represents the music tracks uploaded by users, with metadata like genre, file, and ratings.
3. **Event Model**: Stores event details such as date, time, and location, allowing users to promote their events.
4. **Comment Model**: Allows users to comment on tracks, encouraging interaction.
5. **Follow Model**: Tracks relationships between users for following and notifications.
6. **Rating Model**: Links users and tracks, allowing users to rate tracks.

### Key Functionalities

#### **Authentication and User Management**
- **User Registration and Login**: Using `django-allauth` and JWT for stateless authentication.
- **Profile Management**: Users can create and edit their profiles, uploading images and providing personal details.
- **Permissions**: Only authenticated users can perform certain actions like uploading tracks, commenting, and rating.

#### **Music Upload and Sharing**
- **Track Upload**: Users can upload tracks via a file input form. Uploaded tracks are stored and linked to the user's profile.
- **Discovery Page**: Tracks are displayed on a discovery page, sorted by rating.
- **Sharing**: Once uploaded, tracks are available for sharing and discovery by other users.

#### **Track Rating**
- **Rating System**: Users can rate tracks from 1 to 5 stars. The average rating is updated dynamically.
- **Rating Logic**: The `Track` model calculates the average rating by aggregating individual ratings.

#### **Event Management**
- **Create Events**: Users can create events by providing details such as name, date, location, and genre.
- **Event Sharing**: Events are shown on the user's profile and can be shared with others.
- **Event Filters**: A future feature (currently in development) will allow searching for events based on filters like genre and location.

#### **CRUD Operations**
- **Tracks**: Users can create, read, update, and delete tracks.
- **Events**: Users can manage their events.
- **Profiles**: Users can edit their profiles.
- **Comments**: Users can add and delete comments on tracks.

---

## API Endpoints

### Authentication
- **POST /auth/login/**: Login to the application and receive a JWT token.
- **POST /auth/register/**: Register a new user.
- **POST /auth/logout/**: Log out and invalidate the JWT token.

### User Profile
- **GET /profile/**: Retrieve the authenticated user's profile.
- **PUT /profile/**: Update the authenticated user's profile.

### Tracks
- **GET /tracks/**: Retrieve all tracks.
- **POST /tracks/**: Upload a new track.
- **GET /tracks/{id}/**: Get details of a specific track.
- **PUT /tracks/{id}/**: Update an existing track.
- **DELETE /tracks/{id}/**: Delete a track.

### Events
- **GET /events/**: Retrieve all events.
- **POST /events/**: Create a new event.
- **GET /events/{id}/**: Get details of a specific event.
- **PUT /events/{id}/**: Update an event.
- **DELETE /events/{id}/**: Delete an event.

### Ratings
- **POST /ratings/**: Rate a track (requires track ID and rating).
- **GET /ratings/{id}/**: Get the rating of a specific track.

### Comments
- **POST /comments/**: Add a comment on a track.
- **DELETE /comments/{id}/**: Delete a comment.

---

## Testing

The backend has been tested using Django's built-in test framework. Tests cover various functionalities, including:

- **User Authentication**: Ensuring registration, login, and logout work correctly.
- **Track Upload and Rating**: Verifying users can upload tracks and rate them.
- **Event Creation and Management**: Testing the ability to create, edit, and delete events.
- **CRUD Operations**: Ensuring tracks, profiles, and comments can be managed through API endpoints.
- **Permissions**: Verifying that only authenticated users can access certain features (e.g., uploading tracks, commenting).

Tests are located in the `tests` folder of each app. To run the tests:

```bash
python manage.py test

