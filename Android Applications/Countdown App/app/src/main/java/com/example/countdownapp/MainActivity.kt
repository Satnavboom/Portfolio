package com.example.countdownapp

import android.Manifest
import android.annotation.SuppressLint
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.CountDownTimer
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import com.example.countdownapp.ui.theme.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Settings

@Suppress("DEPRECATION")
class MainActivity : ComponentActivity() {

    private val notificationPermissionRequestCode = 1

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
            != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                notificationPermissionRequestCode)
        } else {
            createNotificationChannel()
        }

        setContent {
            var darkTheme by remember { mutableStateOf(true) }
            var selectedTypography by remember { mutableStateOf(ArialTypography) }
            var showFontDialog by remember { mutableStateOf(false) }

            CountdownAppTheme(darkTheme = darkTheme, typography = selectedTypography) {
                Scaffold(
                    modifier = Modifier.fillMaxSize(),
                    floatingActionButton = {
                        FloatingActionButton(
                            onClick = { showFontDialog = true },
                            containerColor = if (darkTheme) Color.hsl(0f, 1f, 0.25f) else Color.Red
                        ) {
                            Icon(
                                imageVector = Icons.Filled.Settings,
                                contentDescription = "Settings",
                                tint = Color.Black
                            )
                        }
                    }
                ) { innerPadding ->
                    Column(
                        modifier = Modifier
                            .padding(innerPadding)
                            .fillMaxSize(),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        // Dark/Light mode toggle
                        Row(
                            modifier = Modifier.padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            val textColor = if (darkTheme) {
                                Color.hsl(0f, 1f, 0.25f) // Dark mode color
                            } else {
                                Color.Red // Light mode color
                            }
                            Text(
                                text = "Dark Mode",
                                color = textColor,
                                modifier = Modifier.padding(end = 4.dp),
                                style = ArialTypography.bodyMedium
                            )
                            DarkModeSwitch(
                                checked = darkTheme,
                                onCheckedChange = { darkTheme = it },
                                modifier = Modifier.padding(16.dp)
                            )
                        }

                        CountdownTimer(
                            modifier = Modifier
                                .padding(innerPadding)
                                .fillMaxSize(),
                            context = this@MainActivity,
                            typography = selectedTypography
                        )

                        // Font selection dialog
                        if (showFontDialog) {
                            FontSelectionDialog(
                                onDismiss = { showFontDialog = false },
                                onFontSelected = { typography ->
                                    selectedTypography = typography
                                    showFontDialog = false
                                },
                                isDarkTheme = darkTheme
                            )
                        }
                    }
                }
            }
        }
    }

    @Deprecated("This method has been deprecated in favor of using the Activity Result API...")
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == notificationPermissionRequestCode) {
            if (grantResults.isEmpty() || grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Notification permission is required for this app.", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun createNotificationChannel() {
        val name = "Countdown Timer Channel"
        val descriptionText = "Channel for countdown timer notifications"
        val importance = NotificationManager.IMPORTANCE_DEFAULT
        val channel = NotificationChannel("countdown_channel", name, importance).apply {
            description = descriptionText
        }
        val notificationManager: NotificationManager =
            getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.createNotificationChannel(channel)
    }

    fun sendNotification() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
            != PackageManager.PERMISSION_GRANTED
        ) {
            Toast.makeText(this, "Notification permission not granted.", Toast.LENGTH_SHORT).show()
            return
        }

        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        val pendingIntent: PendingIntent =
            PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)

        val notification = NotificationCompat.Builder(this, "countdown_channel")
            .setSmallIcon(R.drawable.ic_launcher_foreground) // Ensure this drawable exists
            .setContentTitle("Countdown Finished")
            .setContentText("It is over.")
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        with(NotificationManagerCompat.from(this)) {
            notify(1, notification)
        }
    }
}

@SuppressLint("DefaultLocale")
@Composable
fun CountdownTimer(
    modifier: Modifier = Modifier,
    context: Context? = null,
    typography: Typography = ArialTypography
) {
    var inputTime by remember { mutableStateOf("") }
    var timeLeft by remember { mutableLongStateOf(0L) }
    var timerRunning by remember { mutableStateOf(false) }
    var countDownTimer: CountDownTimer? by remember { mutableStateOf(null) }

    fun startTimer() {
        val timeInMillis = inputTime.toLongOrNull()?.times(1000) ?: 0L
        timeLeft = timeInMillis
        timerRunning = true

        countDownTimer?.cancel()

        countDownTimer = object : CountDownTimer(timeInMillis, 1000) {
            override fun onTick(millisUntilFinished: Long) {
                timeLeft = millisUntilFinished
            }

            override fun onFinish() {
                timerRunning = false
                (context as? MainActivity)?.sendNotification()
            }
        }.start()
    }

    fun resetTimer() {
        countDownTimer?.cancel()
        timeLeft = 0L
        timerRunning = false
        inputTime = ""
    }

    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        if (!timerRunning) {
            TextField(
                value = inputTime,
                onValueChange = { inputTime = it },
                label = { Text(
                    text = "Enter time in seconds",
                    style = ArialTypography.bodyMedium,
                    color = Color.Black
                ) },
                textStyle = ArialTypography.bodyMedium.copy(color = Color.hsl(0f, 1f, 0.25f)),
                keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number),
                singleLine = true,
                modifier = Modifier.padding(16.dp)
            )
        }

        val hours = (timeLeft / 3600000) % 24
        val minutes = (timeLeft % 3600000) / 60000
        val seconds = (timeLeft % 60000) / 1000
        Text(
            text = String.format("%02d:%02d:%02d", hours, minutes, seconds),
            color = Color.Red,
            style = typography.bodyLarge // Use the selected typography
        )

        Spacer(modifier = Modifier.height(16.dp))

        Row {
            Button(
                onClick = { startTimer() },
                enabled = inputTime.isNotEmpty() && !timerRunning
            ) {
                Text(
                    text = if (timerRunning) "Counting Down..." else "Start Countdown",
                    color = Color.Black
                )
            }

            Spacer(modifier = Modifier.width(8.dp))

            Button(onClick = { resetTimer() }) {
                Text(
                    text = "Reset",
                    color = Color.Black
                )
            }
        }
    }
}

@Composable
fun DarkModeSwitch(
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Switch(
        checked = checked,
        onCheckedChange = onCheckedChange,
        colors = SwitchDefaults.colors(
            checkedThumbColor = Color.Black,
            uncheckedThumbColor = Color.Black,
            checkedTrackColor = Color.hsl(0f, 1f, 0.25f),
            uncheckedTrackColor = Color.Red
        ),
        modifier = modifier
    )
}

@Composable
fun FontSelectionDialog(
    onDismiss: () -> Unit,
    onFontSelected: (Typography) -> Unit,
    isDarkTheme: Boolean
) {
    val fontOptions = listOf(
        FontOption("Font 1", ArialTypography),
        FontOption("Font 2", GhastlyPanicTypography),
        FontOption("Font 3", HollowDeathTypography),
        FontOption("Font 4", MeltedMonsterTypography),
        FontOption("Font 5", MisteryIlahiTypography)
    )
    val buttonColor = if (isDarkTheme) Color.hsl(0f, 1f, 0.25f) else Color.Red
    val buttonHeight = 60.dp

    AlertDialog(
        onDismissRequest = onDismiss,
        confirmButton = {
            Button(onClick = onDismiss) {
                Text(
                    text = "Close",
                    color = Color.Black
                )
            }
        },
        title = {
            Text(
                text = "Select Font",
                color = Color.hsl(0f, 1f, 0.25f),
                style = MaterialTheme.typography.bodyMedium
            )
        },
        text = {
            Column {
                fontOptions.forEach { fontOption ->
                    Button(
                        onClick = { onFontSelected(fontOption.typography) },
                        modifier = Modifier
                            .padding(vertical = 4.dp)
                            .fillMaxWidth()
                            .height(buttonHeight),
                        colors = ButtonDefaults.buttonColors(containerColor = buttonColor),
                    ) {
                        Text(
                            text = fontOption.name,
                            color = Color.Black,
                            style = fontOption.typography.bodyMedium,
                            modifier = Modifier.align(Alignment.CenterVertically)
                        )
                    }
                }
            }
        },
        containerColor = Color.hsl(0f, 0f, 0.05f)
    )
}

data class FontOption(
    val name: String,
    val typography: Typography
)
