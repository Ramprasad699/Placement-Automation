# Placement Automation

## 📌 Project Overview

Placement Automation is a student placement management application designed to make college placement-drive registration easier and more organized.

Currently, placement drive registration links are often shared through WhatsApp. When many messages and links are shared, students may find it difficult to search for the correct drive, and some eligible opportunities may be missed.

This application provides a centralized platform where students can view placement drives that match their eligibility criteria and register easily.

## 🎯 Problem Statement

Students receive multiple placement-drive registration links through WhatsApp. As messages increase, important links can move up in the chat, making them difficult to find and sometimes causing students to miss eligible placement opportunities.

Additionally, not every student is eligible for every placement drive because companies may have different requirements such as CGPA, branch, graduation year, and other criteria.

## 💡 Proposed Solution

The application collects placement-drive information in one centralized platform.

When a student logs in, the system checks their eligibility and displays only the placement drives they are eligible for.

### Basic Flow

Login → Dashboard → Eligible Drives → Register → Registration Status

## 👨‍🎓 Student Features

* Student login
* Student profile
* CGPA-based eligibility filtering
* Placement-drive dashboard
* View eligible placement drives
* Register for placement drives
* Track registration status
* Receive notifications for relevant drives

## 👨‍💼 Admin Features

* Admin login
* Add and manage placement drives
* Set eligibility criteria for each drive
* View registered students
* View students who have not registered
* Track placement-drive registrations
* Manage registration data
* Export registration information to Excel

## 🏢 Placement Drive Eligibility

The system filters placement drives according to the eligibility criteria defined by the administrator.

For example:

* Student A — CGPA 9.2 → sees drives requiring 9.0 CGPA or below
* Student B — CGPA 8.0 → sees drives requiring 8.0 CGPA or below
* Student C — CGPA 6.5 → sees drives requiring 6.5 CGPA or below

This helps students focus only on relevant opportunities.

## 🗄️ Technology Stack

### Frontend

HTML, CSS, JavaScript

### Backend

Python

### Database

PostgreSQL

### Version Control

Git & GitHub

## 📊 Future Enhancements

* Branch-wise eligibility
* Graduation-year eligibility
* Backlog criteria
* Automated notifications
* Excel integration
* Registration analytics
* Conversion into a desktop/mobile application

## 👥 Project

This project is being developed as a 4th-year academic project with the goal of creating a practical placement-management solution for students and administrators.
