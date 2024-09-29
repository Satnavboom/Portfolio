package com.example.a25squares

import android.annotation.SuppressLint
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.a25squares.ui.theme._25SquaresTheme
import kotlin.random.Random
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            _25SquaresTheme {
                GameScreen()
            }
        }
    }
}

data class SquareState(
    val id: Int,
    var color: Color,
    var clicked: Boolean
)

@SuppressLint("AutoboxingStateCreation")
@Composable
fun GameScreen() {
    val squares = remember { mutableStateListOf(*generateInitialGrid().toTypedArray()) }
    var currentGreenIndex by remember { mutableStateOf(Random.nextInt(25)) }
    var nextYellowIndex by remember { mutableStateOf(Random.nextInt(25)) }
    var squaresLeft by remember { mutableStateOf(25) }
    var startTime by remember { mutableStateOf<Long?>(null) }
    var elapsedTime by remember { mutableStateOf(0L) }
    var timerRunning by remember { mutableStateOf(false) }
    var fastestTime by remember { mutableStateOf("00:00:000") }

    val scope = rememberCoroutineScope()

    LaunchedEffect(timerRunning) {
        while (timerRunning) {
            elapsedTime = (System.currentTimeMillis() - (startTime ?: System.currentTimeMillis()))
            delay(5)
        }
    }

    LaunchedEffect(elapsedTime, squaresLeft) {
        if (squaresLeft == 0 && timerRunning) {
            val formattedElapsedTime = formatTime(elapsedTime)
            if (fastestTime == "00:00:000" || elapsedTime < formatTimeToMillis(fastestTime)) {
                fastestTime = formattedElapsedTime
            }
        }
    }

    LaunchedEffect(squaresLeft) {
        if (squaresLeft == 0 && timerRunning) {
            timerRunning = false
        }
    }

    LaunchedEffect(Unit) {
        resetGame(squares)
        currentGreenIndex = Random.nextInt(25)
        nextYellowIndex = Random.nextInt(25)
        while (nextYellowIndex == currentGreenIndex) {
            nextYellowIndex = Random.nextInt(25)
        }
        squares[currentGreenIndex] = squares[currentGreenIndex].copy(color = Color.Green)
        squares[nextYellowIndex] = squares[nextYellowIndex].copy(color = Color.Yellow)
    }

    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Fastest Time: $fastestTime",
            fontSize = 24.sp,
            modifier = Modifier.padding(16.dp),
            color = Color.Black
        )
        Text(
            text = "Time: ${formatTime(elapsedTime)}",
            fontSize = 20.sp,
            modifier = Modifier.padding(16.dp),
            color = Color.Black
        )
        Text(
            text = "Squares Left: $squaresLeft",
            fontSize = 18.sp,
            modifier = Modifier.padding(8.dp),
            color = Color.Black
        )
        Spacer(modifier = Modifier.height(16.dp))
        Box(
            modifier = Modifier
                .size(350.dp)
                .background(
                    Color.Gray,
                    shape = RoundedCornerShape(40.dp)
                ),
            contentAlignment = Alignment.Center
        ) {
            LazyVerticalGrid(
                columns = GridCells.Fixed(5),
                modifier = Modifier.size(300.dp)
            ) {
                items(squares.size) { index ->
                    Square(
                        squareState = squares[index],
                        onClick = {
                            if (index == currentGreenIndex) {
                                if (startTime == null) {
                                    startTime = System.currentTimeMillis()
                                    timerRunning = true
                                }
                                squares[index] = squares[index].copy(
                                    color = Color.Black,
                                    clicked = true
                                )
                                squaresLeft--

                                if (squaresLeft > 0) {
                                    currentGreenIndex = nextYellowIndex
                                    nextYellowIndex = if (squaresLeft == 1) {
                                        -1
                                    } else {
                                        generateNextYellowIndex(squares, currentGreenIndex)
                                    }
                                    squares[currentGreenIndex] = squares[currentGreenIndex].copy(color = Color.Green)
                                    if (nextYellowIndex != -1) {
                                        squares[nextYellowIndex] = squares[nextYellowIndex].copy(color = Color.Yellow)
                                    }
                                }
                            } else {
                                scope.launch {
                                    resetGame(squares)
                                    currentGreenIndex = Random.nextInt(25)
                                    nextYellowIndex = Random.nextInt(25)
                                    while (nextYellowIndex == currentGreenIndex) {
                                        nextYellowIndex = Random.nextInt(25)
                                    }
                                    squares[currentGreenIndex] = squares[currentGreenIndex].copy(color = Color.Green)
                                    squares[nextYellowIndex] = squares[nextYellowIndex].copy(color = Color.Yellow)
                                    squaresLeft = 25
                                    elapsedTime = 0L
                                    startTime = null
                                    timerRunning = false
                                }
                            }
                        }
                    )
                }
            }
        }
        Spacer(modifier = Modifier.height(16.dp))
        Button(
            onClick = {
                resetGame(squares)
                currentGreenIndex = Random.nextInt(25)
                nextYellowIndex = Random.nextInt(25)
                while (nextYellowIndex == currentGreenIndex) {
                    nextYellowIndex = Random.nextInt(25)
                }
                squares[currentGreenIndex] = squares[currentGreenIndex].copy(color = Color.Green)
                squares[nextYellowIndex] = squares[nextYellowIndex].copy(color = Color.Yellow)
                squaresLeft = 25
                elapsedTime = 0L
                startTime = null
                timerRunning = false
            },
            colors = ButtonDefaults.buttonColors(
                containerColor = Color.Gray,
                contentColor = Color.Black
            ),
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "Reset Game",
                color = Color.Black // contentColor already sets the Text's color to black, but I included this line to show what color the text is
            )
        }
    }
}

@Composable
fun Square(squareState: SquareState, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .size(60.dp)
            .padding(4.dp)
            .background(
                color = squareState.color,
                shape = RoundedCornerShape(14.dp)
            )
            .clickable(enabled = !squareState.clicked) { onClick() }
    )
}

fun generateInitialGrid(): List<SquareState> {
    return List(25) { index ->
        SquareState(
            id = index,
            color = Color.DarkGray,
            clicked = false
        )
    }
}

fun resetGame(squares: MutableList<SquareState>) {
    squares.forEach {
        it.color = Color.DarkGray
        it.clicked = false
    }
}

fun generateNextYellowIndex(squares: List<SquareState>, currentGreenIndex: Int): Int {
    var nextYellowIndex = Random.nextInt(25)
    while (nextYellowIndex == currentGreenIndex || squares[nextYellowIndex].clicked) {
        nextYellowIndex = Random.nextInt(25)
    }
    return nextYellowIndex
}

@SuppressLint("DefaultLocale")
fun formatTime(milliseconds: Long): String {
    val totalSeconds = milliseconds / 1000
    val minutes = totalSeconds / 60
    val seconds = totalSeconds % 60
    val millis = milliseconds % 1000
    return String.format("%02d:%02d:%03d", minutes, seconds, millis)
}

fun formatTimeToMillis(time: String): Long {
    val parts = time.split(":")
    val minutes = parts[0].toLong()
    val seconds = parts[1].toLong()
    val millis = parts[2].toLong()
    return (minutes * 60 * 1000) + (seconds * 1000) + millis
}

@Preview(showBackground = true)
@Composable
fun GameScreenPreview() {
    _25SquaresTheme {
        GameScreen()
    }
}