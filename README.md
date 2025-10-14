# Software Requirements Specification Document

## Political App

**Authors:** Brady, Rudra, Lucas  
**Date:** 9/25/25

Submitted in partial fulfillment of the requirements of  
_IT 426 – Advanced Software Engineering_

---

## Table of Contents

1. [Introduction](#introduction)  
    1.1 [Purpose](#purpose)  
    1.2 [Scope](#scope)  
    1.3 [Definitions, Acronyms, and Abbreviations](#definitions-acronyms-and-abbreviations)  
    1.4 [References](#references)  
    1.5 [Overview](#overview)  
2. [General Description](#general-description)  
    2.1 [Product Perspective](#product-perspective)  
    2.2 [User Characteristics](#user-characteristics)  
    2.3 [System Environment](#system-environment)  
    2.4 [Assumptions and Dependencies](#assumptions-and-dependencies)  
3. [Specific Requirements](#specific-requirements)  
    3.1 [Functional Requirements](#functional-requirements)  
    3.2 [Non-Functional Requirements](#non-functional-requirements)  
4. [Feature List](#feature-list)

---

## 1. Introduction

The following sections of the Software Requirements Specification (SRS) provide an overview of the Political App, its goals, environment, and user characteristics. This document sets the foundation for understanding the app’s requirements.

### 1.1 Purpose

The purpose of this SRS is to clearly define both the functional requirements (features the app must provide) and the non-functional requirements (such as performance and security) of the Political App.

### 1.2 Scope

The Political App allows users to create accounts, access representatives’ information, review voting history, view bills, and participate in mock votes. It does **not** support real voting or donations.

### 1.3 Definitions, Acronyms, and Abbreviations

- **SRS** – Software Requirements Specification  
- **UI** – User Interface  
- **API** – Application Programming Interface  

### 1.4 References

- IEEE Guide to Software Requirements Specification (ANSI/IEEE Std. 830-1984)
- Course materials for IT 426 – Advanced Software Engineering

### 1.5 Overview

This document is organized into three major sections: Introduction, General Description, and Specific Requirements. Each section details the system’s goals, environment, user characteristics, and both functional and non-functional requirements.

---

## 2. General Description

This section provides a high-level overview of the Political App, describing the general factors that influence the product and its requirements.

### 2.1 Product Perspective

The Political App is a standalone cross-platform mobile application (Android/iOS). It differs from similar apps by providing mock voting and donation tracking as an educational tool rather than as part of any official government process.

### 2.2 User Characteristics

Target users include students, educators, and citizens interested in politics. Users may have varying levels of technical expertise, from beginner smartphone users to experienced app users.

### 2.3 System Environment

The system will be deployed as a cross-platform mobile app (Android/iOS) and will connect to cloud services for storing user data, bills, and voting results.

### 2.4 Assumptions and Dependencies

- **Assumptions:** Users will have reliable internet access.
- **Dependencies:** Cloud hosting provider, secure authentication services, and APIs for political data sources.

---

## 3. Specific Requirements

This section details the essential features and behaviors of the Political App.

### 3.1 Functional Requirements

#### 3.1.1 Create Account and Login

- **Description:** Users must be able to create an account (name, email, password) and log in securely.
- **Actors:** User, Authentication Service
- **Trigger:** User selects Sign Up or Log In
- **Pre-condition:** User has access to the application
- **Post-condition:** User is authenticated, and a session is created
- **Exceptions:** Invalid credentials, duplicate accounts, server downtime

#### 3.1.2 View Representative and Senator Information

- **Description:** Retrieve and display information about representatives and senators based on user location or input.
- **Actors:** User, Political Data API
- **Trigger:** User selects View Representatives
- **Pre-condition:** User is logged in
- **Post-condition:** Display names, offices, party affiliation
- **Exceptions:** Missing/unavailable data

#### 3.1.3 View Voting History

- **Description:** View voting history of representatives and senators.
- **Actors:** User, Political Data API
- **Trigger:** User selects Voting History
- **Pre-condition:** User selects a representative
- **Post-condition:** Display voting history in chronological order
- **Exceptions:** Limited/outdated data

#### 3.1.4 View Recent Bills

- **Description:** List recent bills with details (bill number, summary, status).
- **Actors:** User, Political Data API
- **Trigger:** User selects Recent Bills
- **Pre-condition:** User is logged in
- **Post-condition:** Bills are displayed with details
- **Exceptions:** Data unavailable/service interruption

#### 3.1.5 Cast Mock Vote on Bill

- **Description:** Users cast mock votes on bills.
- **Actors:** User, Application Database
- **Trigger:** User selects a bill and submits a vote (Yes, No, Abstain)
- **Pre-condition:** User is logged in, selects a bill
- **Post-condition:** Vote is recorded, results updated
- **Exceptions:** Duplicate votes, connection/database errors

#### 3.1.6 View Current Mock Vote Results

- **Description:** Display aggregated results of mock voting on a bill.
- **Actors:** User, Application Database
- **Trigger:** User selects View Results
- **Pre-condition:** At least one vote has been cast
- **Post-condition:** Results shown as percentages/counts
- **Exceptions:** No votes cast yet

### 3.2 Non-Functional Requirements

#### 3.2.1 Performance

- Must deliver smooth and responsive performance for at least 500 concurrent users.

#### 3.2.2 Reliability

- Ensure votes, comments, and account data are stored accurately and transactions complete successfully.

#### 3.2.3 Availability

- Must maintain at least 99.5% uptime per month, especially during peak election periods.

#### 3.2.4 Security

- Strong password policies, secure authentication, and protection of sensitive information.

#### 3.2.5 Maintainability

- Modular codebase for easy updates and improvements.

#### 3.2.6 Portability

- Accessible on both Android and iOS with minimal platform-specific adjustments.

---

## 4. Feature List

- View list of bills
- View congressmen
- View specific bill
- View bill summary
- View bill comments
- Make bill comment
- View election map
- Take civics quiz

---
