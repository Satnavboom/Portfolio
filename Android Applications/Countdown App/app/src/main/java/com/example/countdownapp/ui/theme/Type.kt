package com.example.countdownapp.ui.theme

import com.example.countdownapp.R
import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.font.FontWeight

// Define custom fonts
val ArialFontFamily = FontFamily(
    Font(R.font.arial)
)

val GhastlyPanicFontFamily = FontFamily(
    Font(R.font.ghastlypanic)
)

val HollowDeathFontFamily = FontFamily(
    Font(R.font.hollowdeath)
)

val MeltedMonsterFontFamily = FontFamily(
    Font(R.font.meltedmonster)
)

val MisteryIlahiFontFamily = FontFamily(
    Font(R.font.misteryilahi)
)

// Set of Material typography styles to start with
val ArialTypography = Typography(
    bodyLarge = TextStyle(
        fontFamily = ArialFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 50.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = ArialFontFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 24.sp
    )
)

val GhastlyPanicTypography = Typography(
    bodyLarge = TextStyle(
        fontFamily = GhastlyPanicFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 50.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = GhastlyPanicFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 24.sp
    )
)

val HollowDeathTypography = Typography(
    bodyLarge = TextStyle(
        fontFamily = HollowDeathFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 50.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = HollowDeathFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 24.sp
    )
)

val MeltedMonsterTypography = Typography(
    bodyLarge = TextStyle(
        fontFamily = MeltedMonsterFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 50.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = MeltedMonsterFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 24.sp
    )
)

val MisteryIlahiTypography = Typography(
    bodyLarge = TextStyle(
        fontFamily = MisteryIlahiFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 50.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = MisteryIlahiFontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 24.sp
    )
)