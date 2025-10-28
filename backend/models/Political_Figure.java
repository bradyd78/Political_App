package backend.models;

import java.io.Serializable;
import java.util.Objects;

/**
 * Simple model for a political figure.
 * Keep business logic in the controller/service layer.
 */
public class Political_Figure implements Serializable {
    private static final long serialVersionUID = 1L;

    private Long id;
    private String name;
    private String party;
    private String office;
    private String state;
    private String bio;
    private String imageUrl;

    public Political_Figure() {}

    public Political_Figure(Long id, String name, String party, String office, String state, String bio, String imageUrl) {
        this.id = id;
        this.name = name;
        this.party = party;
        this.office = office;
        this.state = state;
        this.bio = bio;
        this.imageUrl = imageUrl;
    }

    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getParty() { return party; }
    public void setParty(String party) { this.party = party; }

    public String getOffice() { return office; }
    public void setOffice(String office) { this.office = office; }

    public String getState() { return state; }
    public void setState(String state) { this.state = state; }

    public String getBio() { return bio; }
    public void setBio(String bio) { this.bio = bio; }

    public String getImageUrl() { return imageUrl; }
    public void setImageUrl(String imageUrl) { this.imageUrl = imageUrl; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Political_Figure that = (Political_Figure) o;
        return Objects.equals(id, that.id) &&
               Objects.equals(name, that.name) &&
               Objects.equals(party, that.party) &&
               Objects.equals(office, that.office) &&
               Objects.equals(state, that.state) &&
               Objects.equals(bio, that.bio) &&
               Objects.equals(imageUrl, that.imageUrl);
    }
