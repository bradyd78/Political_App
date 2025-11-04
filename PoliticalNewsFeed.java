/*
 * Author: Lucas Paul
 * ULID: lzpaul
 * Date: 10/25/2025
 * File: PoliticalNewsFeed.java
 * Description:
 * Represents a Political News Feed that displays the most recent
 * political news stories to the user. The feed can be populated
 * with news articles provided by the website or user input.
 */

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class PoliticalNewsFeed {

    // --- Inner Class: Represents a News Article ---
    public static class NewsArticle {
        private String title;
        private String content;
        private LocalDateTime timestamp;

        public NewsArticle(String title, String content) {
            this.title = title;
            this.content = content;
            this.timestamp = LocalDateTime.now();
        }

        public String getTitle() {
            return title;
        }

        public String getContent() {
            return content;
        }

        public LocalDateTime getTimestamp() {
            return timestamp;
        }

        @Override
        public String toString() {
            return "📰 " + title + "\n"
                    + "Published: " + timestamp + "\n"
                    + content + "\n";
        }
    }

    // --- Instance Variables ---
    private List<NewsArticle> articles;

    // --- Constructor ---
    public PoliticalNewsFeed() {
        this.articles = new ArrayList<>();
    }

    // --- Methods ---
    public void addArticle(String title, String content) {
        NewsArticle article = new NewsArticle(title, content);
        articles.add(article);
    }

    public void displayRecentNews() {
        if (articles.isEmpty()) {
            System.out.println("No political news is available at this time.\n");
            return;
        }

        // Sort by newest first
        Collections.sort(articles, Comparator.comparing(NewsArticle::getTimestamp).reversed());

        System.out.println("========== Political News Feed ==========\n");
        for (NewsArticle article : articles) {
            System.out.println(article);
            System.out.println("--------------------------------------------\n");
        }
    }

    public NewsArticle getMostRecentArticle() {
        if (articles.isEmpty()) return null;
        Collections.sort(articles, Comparator.comparing(NewsArticle::getTimestamp).reversed());
        return articles.get(0);
    }

    public boolean isEmpty() {
        return articles.isEmpty();
    }
}
