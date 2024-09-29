package com.example.countdownapp.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// Define dark color palette
private val DarkColorPalette = darkColorScheme(
    primary = Color.hsl(0f, 1f, 0.25f),
    secondary = Color.Gray,
    background = Color.Black,
    surface = Color.DarkGray
)

// Define light color palette
private val LightColorPalette = lightColorScheme(
    primary = Color.Red,
    secondary = Color.LightGray,
    background = Color.White,
    surface = Color.Gray
)

@Composable
fun CountdownAppTheme(
    darkTheme: Boolean = true,
    typography: Typography = ArialTypography,
    content: @Composable () -> Unit
) {
    val colors = if (darkTheme) DarkColorPalette else LightColorPalette

    MaterialTheme(
        colorScheme = colors,
        typography = typography, // Referencing Typography from Type.kt
        content = content
    )
}
