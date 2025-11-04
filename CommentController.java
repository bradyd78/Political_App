/*
 * Author: Lucas Paul
 * ULID: lzpaul
 * Date: 10/25/2025
 * File: CommentController.java
 * Description:
 * This class serves as the main controller for the CommentOnBill system.
 * It allows a user to view a list of published Bills, select one, and add a comment to it.
 */

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class CommentController {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        // --- Setup: Example data for Bills and Users ---
        List<Bill> bills = new ArrayList<>();
        bills.add(new Bill("Clean Energy Act", "Encourages renewable energy investments."));
        bills.add(new Bill("Affordable Education Reform", "Provides funding for public universities."));
        bills.add(new Bill("Healthcare for All", "Expands access to affordable healthcare."));

        User user = new User("lucaspaul", "Lucas Paul");

        System.out.println("Welcome, " + user.getUsername() + "!");
        System.out.println("Here are the published bills you can comment on:\n");

        // --- Display Bills ---
        for (int i = 0; i < bills.size(); i++) {
            System.out.println((i + 1) + ". " + bills.get(i).getTitle() + " - " + bills.get(i).getDescription());
        }

        // --- Let the user choose a bill ---
        System.out.print("\nEnter the number of the bill you want to comment on: ");
        int choice = input.nextInt();
        input.nextLine(); // consume newline

        if (choice < 1 || choice > bills.size()) {
            System.out.println("Invalid choice. Exiting...");
            input.close();
            return;
        }

        Bill selectedBill = bills.get(choice - 1);

        // --- Add Comment ---
        System.out.print("Enter your comment: ");
        String commentText = input.nextLine();

        CommentOnBill comment = new CommentOnBill(selectedBill, user, commentText);

        // --- Display Confirmation ---
        System.out.println("\n Your comment has been successfully added!\n");
        comment.displayComment();

        input.close();
    }
}
