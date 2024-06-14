import java.io.* // Import the necessary Java I/O classes
import java.net.Socket // Import the Java Socket class for network communication

fun main() {
    // Server address and port
    val serverAddress = "192.168.144.163" // IP address of the server (localhost in this case)
    val serverPort = 65432 // Port number the server is listening on

    // Initialize socket and streams
    var socket: Socket? = null // Declare a variable to hold the socket connection
    var outputStream: OutputStream? = null // Declare a variable for the output stream
    var inputStream: InputStream? = null // Declare a variable for the input stream

    try {
        // Create a socket to connect to the server
        socket = Socket(serverAddress, serverPort) // Initialize the socket with the server address and port
        println("Connected to server at $serverAddress:$serverPort") // Print a message indicating connection success

        // Get the output stream of the socket
        outputStream = socket.getOutputStream() // Retrieve the output stream from the socket
        val writer = outputStream?.let { PrintWriter(it, true) } // Wrap the output stream in a PrintWriter for easier writing

        // Send a message to the server
        val messageToSend = "Hello, Server!" // Define the message to send to the server
        println("Sending message to server: $messageToSend") // Print the message being sent
        writer?.println(messageToSend) // Send the message through the output stream

        // Get the input stream of the socket
        inputStream = socket.getInputStream() // Retrieve the input stream from the socket
        val reader = BufferedReader(InputStreamReader(inputStream)) // Wrap the input stream in a BufferedReader for easier reading

        // Read the response from the server
        val messageFromServer = reader.readLine() // Read a line of text from the server
        println("Message from server: $messageFromServer") // Print the message received from the server

    } catch (e: IOException) {
        e.printStackTrace() // Print stack trace if an I/O error occurs
    } finally {
        // Close the streams and the socket
        try {
            inputStream?.close() // Close the input stream if it is not null
            outputStream?.close() // Close the output stream if it is not null
            socket?.close() // Close the socket if it is not null
        } catch (e: IOException) {
            e.printStackTrace() // Print stack trace if an I/O error occurs during closing
        }
    }
}
