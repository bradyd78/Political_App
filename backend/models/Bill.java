
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
