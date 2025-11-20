/*
 * Author: Lucas Paul
 * ULID: lzpaul
 * Date: 10/30/2025
 * File: BAPublishesController.java
 * Description:
 * Controller class that allows a user to view either Articles or Blogs
 * that have been published by the website.
 */

import java.util.Scanner;

public class BAPublishesController {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        BAPublishes baPublishes = new BAPublishes();

        // --- Preload Example Articles and Blogs ---
        baPublishes.addPublication("New Tax Policy Announced",
                "The government revealed a new tax policy aimed at supporting small businesses.", "Article");

        baPublishes.addPublication("Understanding the New Voting Bill",
                "A detailed look into the implications of the latest voting rights bill.", "Article");

        baPublishes.addPublication("Behind the Scenes: Policy Reform Journey",
                "A first-hand blog on what it’s like to navigate the policy reform process.", "Blog");

        baPublishes.addPublication("My Experience at the National Debate",
                "An inside story from a young journalist attending the annual national debate.", "Blog");

        boolean running = true;

        // --- Main Menu Loop ---
        while (running) {
            System.out.println("========================================");
            System.out.println("         BA PUBLISHES MENU");
            System.out.println("========================================");
            System.out.println("1. View Published Articles");
            System.out.println("2. View Published Blogs");
            System.out.println("3. Add New Publication");
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
                    baPublishes.displayPublicationsByType("Article");
                    break;

                case 2:
                    baPublishes.displayPublicationsByType("Blog");
                    break;

                case 3:
                    System.out.print("Enter publication type (Article/Blog): ");
                    String type = input.nextLine();
                    System.out.print("Enter title: ");
                    String title = input.nextLine();
                    System.out.print("Enter content: ");
                    String content = input.nextLine();
                    baPublishes.addPublication(title, content, type);
                    System.out.println(type + " published successfully!\n");
                    break;

                case 4:
                    System.out.println("Exiting BA Publishes. Goodbye!");
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
