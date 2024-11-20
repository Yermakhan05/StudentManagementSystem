# Student Management System

## Overview

The Student Management System (SMS) is a Django-based web application designed for managing students, courses, grades, attendance, and user roles. It offers a robust API for handling student data, course enrollments, attendance tracking, and grade management. This project also implements several advanced features such as caching, logging, asynchronous tasks with Celery, and role-based permissions for different types of users.

## Features

- **User Management**: Register, authenticate, and manage users with different roles (Student, Teacher, Admin).
- **Student Management**: Track student records, including profile, enrollment, and attendance.
- **Course Management**: Create and manage courses and enroll students.
- **Grade Management**: Assign grades to students for courses and track performance.
- **Attendance Tracking**: Mark and track student attendance.
- **Email Notifications**: Automated notifications for attendance and grade updates.
- **Asynchronous Tasks**: Use Celery for background tasks such as reminders and periodic reports.
- **Caching**: Optimized data retrieval with Redis caching for frequently accessed data.
- **Logging**: Comprehensive logging for actions like registrations, course enrollments, and grade updates.
- **Testing**: Unit tests for models, views, and Celery tasks.
- **API Documentation**: Automatically generated documentation using Swagger.
- **Analytics**: Track usage metrics like active users and popular courses.

## Tech Stack

- **Django**: The web framework for developing the application.
- **Django REST Framework**: Used for building the API.
- **Celery**: For handling asynchronous tasks (e.g., reminders, notifications).
- **Redis**: Caching layer and message broker for Celery.
- **SQLite**: The database used for storing data.
- **Swagger (drf-yasg)**: For API documentation.
- **Google Analytics (Optional)**: For tracking user behavior and API usage.
- **Djoser**: For handling user registration and authentication.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Yermakhan05/StudentManagementSystem.git
cd StudentManagementSystem
