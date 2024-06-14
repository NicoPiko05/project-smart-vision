package com.example.myapplication

import android.content.Intent
import android.os.Bundle
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
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
import androidx.core.app.NotificationManagerCompat
import com.example.myapplication.ui.theme.MyApplicationTheme
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.*
import java.net.Socket

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Check if the user has granted the "Notification access" permission
        if (!isNotificationServiceEnabled()) {
            // If not, open the system settings where the user can grant the permission
            val intent = Intent("android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS")
            startActivity(intent)
        }

        setContent {
            MyApplicationTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Greeting("Android")

                    // Call the Composable function that handles the network operation
                    //NetworkOperation()
                }
            }
        }
    }
    private fun isNotificationServiceEnabled(): Boolean {
        val packageNames = NotificationManagerCompat.getEnabledListenerPackages(this)
        return packageNames.contains(packageName)
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

class MyNotificationListenerService : NotificationListenerService() {

    override fun onNotificationPosted(sbn: StatusBarNotification) {
        val notification = sbn.notification
        val extras = notification.extras
        val title = extras.getString("android.title")
        val text = extras.getCharSequence("android.text").toString()

        // Here you can send the notification content to your server
        sendNotificationContentToServer(title + ": " + text)
    }

    private fun sendNotificationContentToServer(messageToSend: String) {
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

            println("Sending message to server: $messageToSend")
            writer.println(messageToSend)

            inputStream = socket.getInputStream()
            val reader = BufferedReader(InputStreamReader(inputStream))

            val messageFromServer = reader.readLine()
            println("Message from server: $messageFromServer")
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