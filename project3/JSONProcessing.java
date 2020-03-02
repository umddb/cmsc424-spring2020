import java.sql.*;
import java.util.Scanner;
import org.json.simple.*;

public class JSONProcessing 
{
	public static void processJSON(String json) {
		/************* 
		 * Add you code to insert appropriate tuples into the database.
		 ************/
		System.out.println("Adding data from " + json + " into the database");
	}

	public static void main(String[] argv) {
		Scanner in_scanner = new Scanner(System.in);

		while(in_scanner.hasNext()) {
			String json = in_scanner.nextLine();
			processJSON(json);
		}
	}
}
