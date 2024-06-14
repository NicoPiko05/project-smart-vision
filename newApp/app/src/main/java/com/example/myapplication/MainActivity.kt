package com.example.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.myapplication.ui.theme.MyApplicationTheme
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.*
import java.net.Socket

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApplicationTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Greeting("Android")

                    // Call the Composable function that handles the network operation
                    NetworkOperation()
                }
            }
        }
    }
}

@Composable
fun NetworkOperation() {
    LaunchedEffect(Unit) {
        withContext(Dispatchers.IO) {
            val serverAddress = "192.168.158.223"
            val serverPort = 65432

            var socket: Socket? = null
            var outputStream: OutputStream? = null
            var inputStream: InputStream? = null

            try {

                socket = Socket(serverAddress, serverPort)
                println("Connected to server at $serverAddress:$serverPort")

                outputStream = socket.getOutputStream()
                val writer = PrintWriter(outputStream, true)
                while(true) {
                    val messageToSend = "Hello, Server!"
                    println("Sending message to server: $messageToSend")
                    writer.println(messageToSend)

                    inputStream = socket.getInputStream()
                    val reader = BufferedReader(InputStreamReader(inputStream))

                    val messageFromServer = reader.readLine()
                    println("Message from server: $messageFromServer")
                }
            } catch (e: IOException) {
                e.printStackTrace()
            } finally {
                try {
                    inputStream?.close()
                    outputStream?.close()
                    socket?.close()
                } catch (e: IOException) {
                    e.printStackTrace()
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MyApplicationTheme {
        Greeting("Android")
    }
}
