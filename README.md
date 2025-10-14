Software Requirements Specification Document 
 

Political App 

{1} 

{9/25/25} 

 

{Brady, Rudra, Lucas} 

 

Submitted in partial fulfillment of the requirements of 

IT 426 – Advanced Software Engineering 

 

 

  

Table of Contents									2 

1. Introduction									3 
1.1 Purpose									                  3 
1.2 Scope											3 
1.3 Definitions, Acronyms, and Abbreviations						                 3            1.4 References									                 3 
1.5 Overview									                 4 

2. General Description							             4 
2.1 Product Perspective									4 
2.2 User Characteristics									4 
2.3 System Environment									4 
2.4 Assumptions and Dependencies								4 

3. Specific Requirements								5 
3.1 Functional Requirements								 5 
3.1.1 {Create Account and Login}								 6 
3.1.2 {View Representative and Senator Information}						 6 

3.1.3{View Voting History}									 6 

3.1.4{View recent Bills}									  7 

3.1.5{Cast mock Vote on Bills}								  7 

3.1.6{View current mock vote results}							  7 

 

 
3.2 Non-Functional Requirements							  8 
3.2.1 Performance										   8 
3.2.2 Reliability										   8 
3.2.3 Availability										   8 
3.2.4 Security										   8 
3.2.5 Maintainability									   9 
3.2.6 Portability										   9 

 

  

1. Introduction 

The following subsections of the Software Requirements Specification (SRS) provide an overview of the entire document and set the foundation for understanding the Political App. The purpose of this section is to describe why the system is being developed, what it aims to achieve, and the intended audience for the document. It is important to keep in mind that the SRS defines what the system must do so that designers, developers, and testers can later build and validate the system according to these requirements. 

1.1 Purpose 

The purpose of this Software Requirements Specification (SRS) is to clearly define both the functional requirements (what features the app must provide) and the non-functional requirements (such as performance, security, and availability) for the Political App. This app is being designed as a tool to increase civic engagement by allowing users to explore information about their representatives, view voting histories, learn about current bills, and participate in mock voting activities. 

1.2 Scope 

The Political App is designed to allow users to create accounts, access representatives’ information, review voting history, view bills, and participate in mock votes. It will not support real voting or financial transactions beyond mock donation tracking. The app’s objectives are to improve civic engagement, provide transparency, and educate users on political processes. 

1.3 Definitions, Acronyms, and Abbreviations 

SRS – Software Requirements Specification 
UI – User Interface 
API – Application Programming Interface 

1.4 References 

IEEE Guide to Software Requirements Specification (ANSI/IEEE Std. 830-1984) 
Course materials for IT 426 – Advanced Software Engineering 

1.5 Overview 

This document is organized into three major sections: Introduction, General Description, and Specific Requirements. Each section details the system’s goals, environment, user characteristics, and both functional and non-functional requirements. 

2. General Description 

This section provides a high-level overview of the Political App, describing the general factors that influence the product and its requirements. The focus here is not on detailed specifications, but on clarifying the environment, assumptions, and context in which the system will operate. By outlining the product perspective, intended users, operating environment, and key assumptions, this section sets the foundation for understanding the more specific requirements presented in later sections.  

2.1 Product Perspective 

The Political App is a standalone mobile application. It differs from similar apps by providing mock voting and donation tracking as an educational tool rather than as part of any official government process. 

2.2 User Characteristics 

Target users include students, educators, and citizens with an interest in politics. Users may have varying levels of technical expertise, from beginner smartphone users to experienced app users. 

2.3 System Environment 

The system will be deployed as a cross-platform mobile app (Android/iOS). It will connect to cloud services for storing user data, bills, and voting results. 

2.4 Assumptions and Dependencies 

Assumptions: Users will have reliable internet access. Dependencies: Cloud hosting provider, secure authentication services, and APIs for political data sources. 

  

3. Specific Requirements 

This section provides a high-level overview of the Political App, describing the general factors that influence the product and its requirements. The focus here is not on detailed specifications, but on clarifying the environment, assumptions, and context in which the system will operate. By outlining the product perspective, intended users, operating environment, and key assumptions, this section sets the foundation for understanding the more specific requirements presented in later sections. 

3.1 Functional Requirements 

This section describes the functional requirements of the Political App. These requirements define the essential features and behaviors of the system that enable users to interact with the application. Each requirement is expressed in terms of use cases, which illustrate how users and the system interact to achieve specific goals. 

3.1.1 {Create Account and Login} 

    Description: Users must be able to create an account with basic information (name, email, password) and log in securely. 

    Actor(s): User, Authentication Service. 

    Trigger: User selects Sign Up or Log In from the app interface. 

    Conditions: 

    Pre-condition: User has access to the application. 

    Post-condition: User is authenticated, and a session is created. 

    Exceptions: Invalid login credentials, duplicate accounts, or server downtime. 

3.1.2 {View Representative and Senator Information} 

    Description: The app retrieves and displays information about the user’s representatives and senators based on their location or input. 

    Actor(s): User, Political Data API. 

    Trigger: User selects View Representatives from the menu. 

    Conditions: 

    Pre-condition: User has successfully logged into the app. 

    Post-condition: The app displays representative names, offices, and party affiliation. 

    Exceptions: Missing or unavailable data from external sources. 

3.1.3 {View Voting History} 

    Description: Users can view the voting history of their representatives and senators. 

    Actor(s): User, Political Data API. 

    Trigger: User selects Voting History for a chosen representative. 

    Conditions: 

    Pre-condition: User has selected a representative. 

    Post-condition: Voting history is displayed in chronological order. 

    Exceptions: Limited or outdated external data. 

3.1.4 {View Recent Bills} 

    Description: The app lists recent bills introduced in Congress, with details including bill number, summary, and status. 

    Actor(s): User, Political Data API. 

    Trigger: User selects Recent Bills from the menu. 

    Conditions: 

    Pre-condition: User is logged in. 

    Post-condition: Bills are displayed with accessible details. 

    Exceptions: External data not available or service interruption. 

3.1.5 {Cast Mock Vote on Bill} 

    Description: Users may cast a mock vote on bills and view how other users have voted. 

    Actor(s): User, Application Database. 

    Trigger: User selects a bill and submits a mock vote (Yes, No, Abstain). 

    Conditions: 

    Pre-condition: User is logged in and selects a bill. 

    Post-condition: The vote is recorded in the database and updates the overall results. 

    Exceptions: Duplicate votes, connection issues, or database errors. 

3.1.6 {View Current Mock Vote Results} 

    Description: Displays the aggregated results of mock voting on a selected bill. 

    Actor(s): User, Application Database. 

    Trigger: User selects View Results for a bill. 

    Conditions: 

    Pre-condition: At least one vote has been cast. 

    Post-condition: Results are shown as percentages or counts. 

Exceptions: No votes cast yet for a bill. 

 

 

 

3.2 Non-Functional Requirements 

3.2.1 Performance 

    The Political App must deliver smooth and responsive performance even under heavy load. The system should be able to handle at least 500 concurrent users actively browsing bills, news, and casting mock votes while keeping the average response time under 2 seconds. This ensures that users experience minimal delays and can complete their tasks without frustration. To maintain this performance, the system will rely on efficient database queries, caching frequently accessed data, and using cloud-based scaling to manage sudden spikes in activity, especially around election season when user demand will be highest. 

3.2.2 Reliability 

    Reliability is critical to maintaining user trust. The app must ensure that votes, comments, and account data are stored accurately without loss or corruption. Transactions should complete successfully with an error rate below 0.1%. In practice, this means that if a user casts a mock vote or posts a comment, it should always be reflected correctly in the system. Regular backups and testing will help preserve data in the event of system issues. 

3.2.3 Availability 

    During peak election periods, users may access the app at any time of day. To meet this demand, the app must maintain at least 99.5% uptime per month, which translates to only a few hours of allowable downtime.  

3.2.4 Security 

    Security is a top priority because the system will handle user accounts and potentially sensitive information like mock donation records. Strong password policies and secure authentication methods will further protect user accounts. 

3.2.5 Maintainability 

    The Political App should be easy to update as new election features or improvements are needed. The codebase must be modular, meaning each feature is separated into smaller components that can be changed without disrupting the entire system. Developers should document their code thoroughly, making it easier for new team members to understand and contribute. Bug fixes should be addressed quickly, with a target turnaround of under 48 hours for most issues. This will keep the app running smoothly and responsive to feedback. 

3.2.6 Portability 

    The app should be accessible to a wide audience, regardless of device type. It will be developed to run on both Android and iOS with minimal platform-specific adjustments. This cross-platform approach ensures users are not excluded based on their device. The design will also consider different screen sizes and operating system versions so that the experience remains consistent and usable across a variety of mobile devices. 

 

View list of bills 

View congressmen 

View Specific Bill 

View bill summary 

View Bill comments 

Make bill comment 

View election map 

Take civics quiz 

 
