/*
* objectserverSchemaDump.java
*
* Created on May 16, 2004, 9:01 PM
*/

/**
*
* @author  Dan Roscigno
*
* Use the Netcool specific copy of jconn3 that ships with Netcool OMNIbus
* I found it in $OMNIHOME/java/jars/jconn3.jar
*
* export CLASSPATH=.:$CLASSPATH:./jconn3.jar 
* javac objectserverSchemaDump.java 
* remember to escape special chars in the password.  Default port is 4100
* java objectserverSchemaDump  alerts.status root "T\@psecret" hostname port

*/
import java.sql.*;
import com.sybase.jdbc3.jdbc.*;


public class objectserverSchemaDump {
	/**
	* @param args the command line arguments
	*/
	public static void main( String[] args ) {
		if (args.length < 5) {
			System.out.println("Usage: java objectserverSchemaDump <tablename> <username> <password> <hostname> <port>");
			System.exit(0);
		} // end if args.length ...
		String tablename = args[0];
		String username = args[1];
		String password = args[2];
		String hostname = args[3];
		String port = args[4];

		try {

			// Uses Sybase jConnect 5.2.  You can get this from http://www.sybase.com,
			// search for "JDBC jconnect 5.2 software download" and click on the 'Downloads' link
			Class.forName("com.sybase.jdbc3.jdbc.SybDriver");
			String connString = "jdbc:sybase:Tds:" + hostname + ":" + port;

			//Connection conn = DriverManager.getConnection("jdbc:sybase:Tds:192.168.111.128:4101", "root", "");
			Connection conn = DriverManager.getConnection(connString, username, password);
			Statement stmt = conn.createStatement( );

			ResultSet rs = stmt.executeQuery( "describe " + tablename + ";");
			System.out.println("Columns are:");
			while ( rs.next( ) ) {
				String result =  rs.getString( 1 );
				System.out.println("\t" + result);
			}
			System.out.println("");

			rs = stmt.executeQuery( "select * from " + tablename + ";");
			// Get the metadata
			ResultSetMetaData md = rs.getMetaData() ;

			while ( rs.next( ) ) {

				System.out.print( "insert into " + tablename + " values (");
				// Print the column labels and types
				for( int i = 1; i <= md.getColumnCount(); i++ ) {
					//System.out.print( md.getColumnLabel(i) + ":" + md.getColumnClassName(i) + " " + rs.getString(i)) ;
					if (md.getColumnClassName(i).equals("java.lang.String")){
						System.out.print( "'" + rs.getString(i).trim() + "'");
						} else {
							System.out.print(rs.getString(i));
						}
						if (i < md.getColumnCount()){
							System.out.print(", ");
						}
					}
					System.out.println(");") ;

				} // end while
			} //end try

			catch ( SQLException  sqe ) {

				System.out.println("Unexpected  exception : " +
				sqe.toString() + ",  sqlstate = " +
				sqe.getSQLState());

			}
			catch ( Exception e) {
				System.out.println( "An exception occurred." + e );
			}
		} // end of main

	} // end of objectserverSchemaDump class
