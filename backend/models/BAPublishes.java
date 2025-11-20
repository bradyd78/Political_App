/*
 * Author: Lucas Paul
 * ULID: lzpaul
 * Date: 10/30/2025
 * File: BAPublishes.java
 * Description:
 * This class represents the publishing system for the website.
 * It allows the user to view either Articles or Blogs that have
 * been published, based on their selected choice.
 */

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class BAPublishes {

    // --- Inner Class: Represents a Published Item (Article or Blog) ---
    public static class Publication {
        private String title;
        private String content;
        private String type; // "Article" or "Blog"
        private LocalDateTime timestamp;

        public Publication(String title, String content, String type) {
            this.title = title;
            this.content = content;
            this.type = type;
            this.timestamp = LocalDateTime.now();
        }

        public String getTitle() {
            return title;
        }

        public String getContent() {
            return content;
        }

        public String getType() {
            return type;
        }

        public LocalDateTime getTimestamp() {
            return timestamp;
        }

        @Override
        public String toString() {
            return "📰 " + type.toUpperCase() + ": " + title + "\n"
                    + "Published: " + timestamp + "\n"
                    + content + "\n";
        }
    }

    // --- Instance Variables ---
    private List<Publication> publications;

    // --- Constructor ---
    public BAPublishes() {
        this.publications = new ArrayList<>();
    }

    // --- Methods ---

    // Add a new article or blog
    public void addPublication(String title, String content, String type) {
        publications.add(new Publication(title, content, type));
    }

    // Display all publications of a given type (Article or Blog)
    public void displayPublicationsByType(String type) {
        List<Publication> filtered = new ArrayList<>();
        for (Publication pub : publications) {
            if (pub.getType().equalsIgnoreCase(type)) {
                filtered.add(pub);
            }
        }

        if (filtered.isEmpty()) {
            System.out.println("No " + type.toLowerCase() + "s available at this time.\n");
            return;
        }

        // Sort by newest first
        Collections.sort(filtered, Comparator.comparing(Publication::getTimestamp).reversed());

        System.out.println("========== 📢 Published " + type + "s ==========\n");
        for (Publication pub : filtered) {
            System.out.println(pub);
            System.out.println("--------------------------------------------\n");
        }
    }

    // Return true if there are no publications
    public boolean isEmpty() {
        return publications.isEmpty();
    }
}
