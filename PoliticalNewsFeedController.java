/*
 * Author: Lucas Paul
 * ULID: lzpaul
 * Date: 10/26/2025
 * File: PoliticalNewsFeedController.java
 * Description:
 * Controller class for interacting with the PoliticalNewsFeed.
 * Allows the user to view, add, and display the most recent political news.
 */

import java.util.Scanner;

public class PoliticalNewsFeedController {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        PoliticalNewsFeed feed = new PoliticalNewsFeed();

        // --- Preload some example articles from the website ---
        feed.addArticle("Senate Approves Clean Energy Initiative",
                "A major step toward sustainable infrastructure has passed with bipartisan support.");
        feed.addArticle("Education Funding Increased Nationwide",
                "New legislation will allocate more resources to public schools and teacher salaries.");
        feed.addArticle("Healthcare Access Expands for Rural Communities",
                "Rural areas to receive new clinics and telehealth funding in the upcoming fiscal year.");

        boolean running = true;

        // --- Main Menu Loop ---
        while (running) {
            System.out.println("========================================");
            System.out.println("     POLITICAL NEWS FEED MENU");
            System.out.println("========================================");
            System.out.println("1. View all recent political news");
            System.out.println("2. Add a new news article");
            System.out.println("3. View the most recent article");
            System.out.println("4. Exit");
            System.out.print("Enter your choice: ");

            int choice;
            try {
                choice = Integer.parseInt(input.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a number.\n");
                continue;
            }

            switch (choice) {
                case 1:
                    feed.displayRecentNews();
                    break;

                case 2:
                    System.out.print("Enter news title: ");
                    String title = input.nextLine();
                    System.out.print("Enter news content: ");
                    String content = input.nextLine();
                    feed.addArticle(title, content);
                    System.out.println("News article added successfully!\n");
                    break;

                case 3:
                    if (feed.isEmpty()) {
                        System.out.println("No news articles to display.\n");
                    } else {
                        System.out.println("Most Recent Article:\n");
                        System.out.println(feed.getMostRecentArticle());
                    }
                    break;

                case 4:
                    System.out.println("Exiting Political News Feed. Goodbye!");
                    running = false;
                    break;

                default:
                    System.out.println("Invalid choice. Please select 1–4.\n");
                    break;
            }
        }

        input.close();
    }
}
