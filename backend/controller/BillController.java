import org.springframework.web.bind.annotation.*;
import java.util.*;

public class BillController{

  private Map<Integer, Bill> billStore = new HashMap<>();

  //Create a new Bill
  public Bill createBill(Bill bill){
    billStore.put(bill.getBillID(), bill);
    return bill;
  }

  public Bill getBill(int id){
    return billStore.get(id);
  }

  public Collection<Bill> getAllBills(){
    return billStore.values();
  }

  //Vote on a Bill
  public String voteOnBill(int id, boolean inFavor){
    Bill bill = billStore.get(id);
    if(bill == null) return "Bill not found.";
    bill.voteOnBill(inFavor);
    return "Vote recorded. Current support: " + bill.showVotePercent() + "%";
  }

  

  

}
