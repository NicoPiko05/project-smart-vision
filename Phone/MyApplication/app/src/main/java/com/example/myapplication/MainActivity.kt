package com.example.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.myapplication.ui.theme.MyApplicationTheme
import java.io.BufferedReader
import java.io.DataOutputStream
import java.io.InputStreamReader
import java.io.PrintWriter
import java.net.Socket

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
        }
    }
}



fun SendTcpData() {

    try {
        println("in the block")
        val client = Socket("192.168.231.80", 10222);
        val dout = DataOutputStream(client.getOutputStream());

        println("client created")


        dout.writeUTF("Yippie");

        dout.flush()
        dout.close()
        client.close()
    }
    catch (e:Exception){
        println(e)
    }
}
@Composable
@Preview
fun Ui(modifier: Modifier = Modifier){
    Button(onClick = { SendTcpData() }) {

    }
}
