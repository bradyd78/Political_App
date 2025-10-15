import java.util.List;
import java.util.ArrayList;

public class PoliticalAppManager {
    private List<Bill> bills;
    private List<PoliticalFigure> figures;

    public PoliticalAppManager() {
        bills = new ArrayList<>();
        figures = new ArrayList<>();
    }

    // Bill management
    public void addBill(Bill bill) {
        bills.add(bill);
    }

    public List<Bill> getAllBills() {
        return new ArrayList<>(bills);
    }

}