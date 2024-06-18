package com.example.projectVision

import java.io.BufferedReader
import java.io.IOException
import java.io.InputStream
import java.io.InputStreamReader
import java.io.OutputStream
import java.io.PrintWriter
import java.net.Socket

class Connection {
    object ServerConnection{
        val serverAddress = "192.168.158.223"
        val serverPort = 65432
        var socket: Socket? = null
        var outputStream: OutputStream? = null
        var inputStream: InputStream? = null
        var writer: PrintWriter? = null
        var reader: BufferedReader? = null
        var recievedMessage: String? = null

        @Synchronized
        fun connect(): Boolean {
            val thread = Thread {
                try {
                    socket = Socket(serverAddress, serverPort)
                    outputStream = socket?.getOutputStream()
                    inputStream = socket?.getInputStream()
                    writer = outputStream?.let { PrintWriter(it, true) }
                    reader = BufferedReader(InputStreamReader(inputStream))

                } catch (e: IOException) {
                    e.printStackTrace()
                }
            }
            thread.start()
            return try{
                thread.join()
                socket != null
            } catch (e: InterruptedException) {
                e.printStackTrace()
                false
            }
        }
        @Synchronized
        fun sendMessage(messageToSend: String){
            writer?.println(messageToSend) ?: println("Connection not established")
        }
        @Synchronized
        fun readMessage(){
            recievedMessage = reader?.readLine()
        }
        @Synchronized
        fun close(){
            try{
            inputStream?.close()
            outputStream?.close()
            socket?.close()
        } catch (e: IOException){
                e.printStackTrace()
            }        }

    }
}