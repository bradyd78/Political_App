import org.springframework.web.bind.annotation.*;
import java.util.*;

public class BillController{

  private Map<Integer, Bill> billStore = new HashMap<>();

  //Create a new Bill
  public Bill createBill(Bill bill){
    billStore.put(bill.getBillID(), bill);
    return bill;
  }

  

}
