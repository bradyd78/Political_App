import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class Bill {
    private int billID;
    private String name, summary, fullBill, status;
    private int numberMockVotes, inFavor, against;
    private List<String> comments;
    private Date createdAt; //Timestamp for when the bill was created

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
        this.createdAt = new Date(); //Set creation time to now
    }

    public int getBillID() {
        return billID;
    }

    public String getName() {
        return name;
    }

    public String getSummary() {
        return summary;
    }

    public String getFullBill() {
        return fullBill;
    }

    public String getStatus() {
        return status;
    }

    public int getNumberMockVotes() {
        return numberMockVotes;
    }

    public int getInFavor() {
        return inFavor;
    }

    public int getAgainst() {
        return against;
    }

    public List<String> getComments() {
        return comments;
    }

    public Date getCreatedAt() {
        return createdAt;
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
                ", createdAt=" + createdAt +
                '}';
    }
}

