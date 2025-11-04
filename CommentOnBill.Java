/*
 * Author: Lucas Paul
 * ULID: lzpaul
 * Date: 11/03/2025
 * File: CommentOnBill.java
 * Description: 
 * This class allows a user to post a comment on a Bill that has been published 
 * by the political website. It links the comment to both the Bill and the User 
 * who created it, with timestamp tracking.
 */

import java.time.LocalDateTime;

public class CommentOnBill {
    
    // --- Instance Variables ---
    private int commentId;
    private Bill bill;                // The bill being commented on
    private User user;                // The user who made the comment
    private String commentText;       // Content of the comment
    private LocalDateTime timestamp;  // When the comment was made

    // --- Static Counter (for unique comment IDs) ---
    private static int nextId = 1;

    // --- Constructors ---
    public CommentOnBill(Bill bill, User user, String commentText) {
        this.commentId = nextId++;
        this.bill = bill;
        this.user = user;
        this.commentText = commentText;
        this.timestamp = LocalDateTime.now();
    }

    // --- Getters ---
    public int getCommentId() {
        return commentId;
    }

    public Bill getBill() {
        return bill;
    }

    public User getUser() {
        return user;
    }

    public String getCommentText() {
        return commentText;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    // --- Setters ---
    public void setCommentText(String commentText) {
        this.commentText = commentText;
    }

    // --- Utility Methods ---
    @Override
    public String toString() {
        return "Comment #" + commentId + " on Bill: " + bill.getTitle() + "\n"
                + "By: " + user.getUsername() + " on " + timestamp + "\n"
                + "Comment: " + commentText + "\n";
    }

    // Method to display comment in a formatted way (for console or web output)
    public void displayComment() {
        System.out.println("-------------------------------------------------");
        System.out.println("Bill: " + bill.getTitle());
        System.out.println("User: " + user.getUsername());
        System.out.println("Date: " + timestamp);
        System.out.println("Comment: " + commentText);
        System.out.println("-------------------------------------------------");
    }
}
