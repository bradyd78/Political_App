
package backend;

import java.util.ArrayList;
import java.util.List;

public class Bill {
    private int billID;
    private String name, summary, fullBill, status;
    private int numberMockVotes, inFavor, against;
    private List<String> comments;

    public Bill(int billID, String name, String summary, String fullBill, String status) {
        this.billID = billID;
        this.name = name;
        this.summary = summary;
        this.fullBill = fullBill;
        this.status = status;
        this.numberMockVotes = 0;
        this.inFavor = 0;
        this.against = 0;
        this.comments = new ArrayList<>();
    }

    public double showVotePercent() {
        if (numberMockVotes == 0) return 0.0;
        return (double) inFavor / numberMockVotes * 100;
    }

    public Bill viewBill() {
        // Returns a copy of this bill (could be more meaningful in context)
        return this;
    }

    public List<String> viewCommentsOnBill() {
        return new ArrayList<>(comments);
    }

    public void makeComment(String comment) {
        comments.add(comment);
    }

    public void voteOnBill(boolean vote) {
        numberMockVotes++;
        if (vote) {
            inFavor++;
        } else {
            against++;
        }
    }

    @Override
    public String toString() {
        return "Bill{" +
                "billID=" + billID +
                ", name='" + name + '\'' +
                ", summary='" + summary + '\'' +
                ", fullBill='" + fullBill + '\'' +
                ", status='" + status + '\'' +
                ", numberMockVotes=" + numberMockVotes +
                ", inFavor=" + inFavor +
                ", against=" + against +
                ", comments=" + comments +
                '}';
    }
}
