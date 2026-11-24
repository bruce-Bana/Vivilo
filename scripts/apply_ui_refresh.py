from pathlib import Path

base = Path("source/app/src/main/java/com/vivilo/media/ui/screens/BrowserComponents.kt")
s = base.read_text(encoding="utf-8")
if "import androidx.compose.foundation.border" not in s:
    s = s.replace("import androidx.compose.foundation.background", "import androidx.compose.foundation.background\nimport androidx.compose.foundation.border", 1)

start = s.index("@Composable\nfun FloatingNavPill(")
end = s.index("\n@Composable\nfun FloatingSelectionBar", start)
nav = """@Composable
fun FloatingNavPill(selectedTab: Int, onSelect: (Int) -> Unit) {
    val destinations = listOf(
        NavDestination("Browse", Icons.Default.Explore, "nav_tab_browse"),
        NavDestination("Clean", Icons.Default.CleaningServices, "nav_tab_clean"),
        NavDestination("Playlists", Icons.Default.LibraryMusic, "nav_tab_playlists")
    )
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .navigationBarsPadding()
            .padding(horizontal = 22.dp, vertical = 8.dp),
        contentAlignment = Alignment.Center
    ) {
        Row(
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            destinations.forEachIndexed { index, dest ->
                val selected = selectedTab == index
                val tint = if (selected) MaterialTheme.colorScheme.primary
                    else MaterialTheme.colorScheme.onSurfaceVariant
                Surface(
                    onClick = { onSelect(index) },
                    shape = RoundedCornerShape(17.dp),
                    color = if (selected) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.88f)
                        else MaterialTheme.colorScheme.surface.copy(alpha = 0.78f),
                    shadowElevation = if (selected) 7.dp else 4.dp,
                    modifier = Modifier
                        .size(width = 64.dp, height = 58.dp)
                        .border(
                            width = 1.dp,
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = if (selected) 0.14f else 0.09f),
                            shape = RoundedCornerShape(17.dp)
                        )
                        .testTag(dest.tag)
                ) {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Icon(
                            imageVector = dest.icon,
                            contentDescription = dest.label,
                            tint = tint,
                            modifier = Modifier.size(20.dp)
                        )
                        Spacer(modifier = Modifier.height(3.dp))
                        Text(
                            text = dest.label,
                            style = MaterialTheme.typography.labelSmall,
                            fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
                            color = tint,
                            maxLines = 1
                        )
                    }
                }
            }
        }
    }
}
"""
s = s[:start] + nav + s[end:]

replacements = [
    (""".testTag("home_internal_storage_card"),
                shape = RoundedCornerShape(22.dp),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.65f)
                ),""", """.testTag("home_internal_storage_card")
                    .border(1.dp, MaterialTheme.colorScheme.onSurface.copy(alpha = 0.08f), RoundedCornerShape(18.dp)),
                shape = RoundedCornerShape(18.dp),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.72f)
                ),"""),
    (""".padding(18.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp)""", """.padding(14.dp),
                    verticalArrangement = Arrangement.spacedBy(11.dp)"""),
    (""".size(50.dp)
                                .clip(CircleShape)""", """.size(44.dp)
                                .clip(CircleShape)"""),
    ("""modifier = Modifier.size(28.dp)
                            )
                        }

                        Column(modifier = Modifier.weight(1f))""", """modifier = Modifier.size(24.dp)
                            )
                        }

                        Column(modifier = Modifier.weight(1f))"""),
    ("""shape = RoundedCornerShape(20.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.65f)
                    ),""", """shape = RoundedCornerShape(17.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.68f)
                    ),"""),
    ("""modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(12.dp)""", """modifier = Modifier.padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp)"""),
    (""".size(44.dp)
                                .clip(CircleShape)""", """.size(38.dp)
                                .clip(CircleShape)"""),
    ("""modifier = Modifier.size(24.dp)
                            )
                        }
                        Column {
                            Text("Safe folder""" , """modifier = Modifier.size(21.dp)
                            )
                        }
                        Column {
                            Text("Safe folder"""),
    ("""modifier = Modifier.size(24.dp)
                            )
                        }
                        Column {
                            Text("Favorites""" , """modifier = Modifier.size(21.dp)
                            )
                        }
                        Column {
                            Text("Favorites"""),
    ("""shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)),""", """shape = RoundedCornerShape(15.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.68f)),"""),
    (""".aspectRatio(1f)
            .clip(RoundedCornerShape(16.dp))""", """.aspectRatio(0.94f)
            .clip(RoundedCornerShape(15.dp))"""),
    ("""shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (isSelected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.6f)""", """shape = RoundedCornerShape(15.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (isSelected) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.88f) else MaterialTheme.colorScheme.surface.copy(alpha = 0.70f)"""),
    (""".size(56.dp)
                            .clip(RoundedCornerShape(14.dp))""", """.size(48.dp)
                            .clip(RoundedCornerShape(12.dp))"""),
    (""".size(56.dp)
                            .clip(RoundedCornerShape(14.dp))""", """.size(48.dp)
                            .clip(RoundedCornerShape(12.dp))"""),
    (""".padding(8.dp)
            ) {
                Column {""", """.padding(7.dp)
            ) {
                Column {"""),
    ("""shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (isSelected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface
        )""", """shape = RoundedCornerShape(13.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (isSelected) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.9f) else MaterialTheme.colorScheme.surface.copy(alpha = 0.72f)
        )"""),
    ("""modifier = Modifier.padding(12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(14.dp)""", """modifier = Modifier.padding(horizontal = 11.dp, vertical = 9.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(11.dp)"""),
    (""".size(52.dp)
                    .clip(RoundedCornerShape(12.dp))""", """.size(44.dp)
                    .clip(RoundedCornerShape(11.dp))""")
]
for old, new in replacements:
    if old not in s:
        raise SystemExit("UI refresh expected snippet missing: " + old[:80].replace("\n", " "))
    s = s.replace(old, new, 1)
base.write_text(s, encoding="utf-8")

wallpaper = Path("source/app/src/main/java/com/vivilo/media/ui/components/WallpaperBackground.kt")
w = wallpaper.read_text(encoding="utf-8")
needle = """            }
        }

        content()
"""
replacement = """            }
        } else {
            // Subtle ambient color keeps glass cards legible without costly live blur.
            Canvas(modifier = Modifier.fillMaxSize()) {
                drawCircle(
                    color = MaterialTheme.colorScheme.primary.copy(alpha = 0.055f),
                    radius = size.width * 0.78f,
                    center = Offset(size.width * 0.92f, size.height * 0.08f)
                )
                drawCircle(
                    color = MaterialTheme.colorScheme.tertiary.copy(alpha = 0.045f),
                    radius = size.width * 0.62f,
                    center = Offset(size.width * 0.04f, size.height * 0.88f)
                )
            }
        }

        content()
"""
if needle not in w:
    raise SystemExit("WallpaperBackground insertion point missing")
wallpaper.write_text(w.replace(needle, replacement, 1), encoding="utf-8")
print("Applied compact floating tabs, translucent cards, tighter file tiles and ambient glass backdrop")
