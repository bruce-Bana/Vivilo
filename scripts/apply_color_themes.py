from pathlib import Path

ROOT = Path("source/app/src/main/java/com/vivilo/media")

def replace_once(path: Path, old: str, new: str, label: str):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

prefs = ROOT / "ui/theme/AppPreferences.kt"
replace_once(prefs,
'''    val THEME_MODE = stringPreferencesKey("theme_mode")
    val WALLPAPER = stringPreferencesKey("wallpaper")''',
'''    val THEME_MODE = stringPreferencesKey("theme_mode")
    val COLOR_THEME = stringPreferencesKey("color_theme")
    val WALLPAPER = stringPreferencesKey("wallpaper")''', "color theme preference key")

palette_enum = '''enum class AppColorTheme(
    val label: String,
    val swatch: Color,
    val lightPrimary: Color,
    val lightOnPrimary: Color,
    val lightContainer: Color,
    val lightOnContainer: Color,
    val darkPrimary: Color,
    val darkOnPrimary: Color,
    val darkContainer: Color,
    val darkOnContainer: Color,
    val lightSecondary: Color,
    val darkSecondary: Color
) {
    LIGHT_BLUE("Light Blue", Color(0xFF69AEFF), Color(0xFF2878D0), Color.White, Color(0xFFD9EAFF), Color(0xFF0C315C), Color(0xFFA9CEFF), Color(0xFF12365E), Color(0xFF234B78), Color(0xFFD9EAFF), Color(0xFF56718D), Color(0xFFB8D7F8)),
    OCEAN("Ocean", Color(0xFF28A9C7), Color(0xFF006A83), Color.White, Color(0xFFBCEAF2), Color(0xFF003640), Color(0xFF72D5EA), Color(0xFF003642), Color(0xFF005466), Color(0xFFBCEAF2), Color(0xFF426C78), Color(0xFFB0DDE6)),
    VIOLET("Violet", Color(0xFF9A82E8), Color(0xFF6650B5), Color.White, Color(0xFFE8DDFF), Color(0xFF25145B), Color(0xFFC8B8FF), Color(0xFF35206D), Color(0xFF4B3788), Color(0xFFE8DDFF), Color(0xFF655B80), Color(0xFFD1C4F5)),
    EMERALD("Emerald", Color(0xFF36B99A), Color(0xFF08765F), Color.White, Color(0xFFBCEFE1), Color(0xFF002F25), Color(0xFF75DDBF), Color(0xFF00382C), Color(0xFF005443), Color(0xFFBCEFE1), Color(0xFF4E7066), Color(0xFFB8E0D2)),
    ROSE("Rose", Color(0xFFE58AAA), Color(0xFFAD426E), Color.White, Color(0xFFFFD9E5), Color(0xFF3F1025), Color(0xFFFFAFCB), Color(0xFF561A35), Color(0xFF772C4C), Color(0xFFFFD9E5), Color(0xFF80606C), Color(0xFFF0C3D2))
}

'''
replace_once(prefs, "enum class WallpaperOption(", palette_enum + "enum class WallpaperOption(", "insert color theme palette")

replace_once(prefs,
'''data class AppPreferencesState(
    val themeMode: AppThemeMode = AppThemeMode.SYSTEM,
    val wallpaper: WallpaperOption = WallpaperOption.NONE,''',
'''data class AppPreferencesState(
    val themeMode: AppThemeMode = AppThemeMode.SYSTEM,
    val colorTheme: AppColorTheme = AppColorTheme.LIGHT_BLUE,
    val wallpaper: WallpaperOption = WallpaperOption.NONE,''', "preference state color theme")

replace_once(prefs,
'''                themeMode = prefs[PrefKeys.THEME_MODE]?.let { name ->
                    AppThemeMode.entries.firstOrNull { it.name == name }
                } ?: AppThemeMode.SYSTEM,
                wallpaper = prefs[PrefKeys.WALLPAPER]?.let { name ->''',
'''                themeMode = prefs[PrefKeys.THEME_MODE]?.let { name ->
                    AppThemeMode.entries.firstOrNull { it.name == name }
                } ?: AppThemeMode.SYSTEM,
                colorTheme = prefs[PrefKeys.COLOR_THEME]?.let { name ->
                    AppColorTheme.entries.firstOrNull { it.name == name }
                } ?: AppColorTheme.LIGHT_BLUE,
                wallpaper = prefs[PrefKeys.WALLPAPER]?.let { name ->''', "read saved color theme")

replace_once(prefs,
'''            prefs[PrefKeys.THEME_MODE] = state.themeMode.name
            prefs[PrefKeys.WALLPAPER] = state.wallpaper.name''',
'''            prefs[PrefKeys.THEME_MODE] = state.themeMode.name
            prefs[PrefKeys.COLOR_THEME] = state.colorTheme.name
            prefs[PrefKeys.WALLPAPER] = state.wallpaper.name''', "persist color theme")

replace_once(prefs,
'''interface AppPreferencesController {
    fun updateThemeMode(mode: AppThemeMode)
    fun updateWallpaper(wallpaper: WallpaperOption)''',
'''interface AppPreferencesController {
    fun updateThemeMode(mode: AppThemeMode)
    fun updateColorTheme(theme: AppColorTheme)
    fun updateWallpaper(wallpaper: WallpaperOption)''', "controller color theme API")

replace_once(prefs,
'''            override fun updateThemeMode(mode: AppThemeMode) {
                applyUpdate(state.copy(themeMode = mode))
            }

            override fun updateWallpaper(wallpaper: WallpaperOption) {''',
'''            override fun updateThemeMode(mode: AppThemeMode) {
                applyUpdate(state.copy(themeMode = mode))
            }

            override fun updateColorTheme(theme: AppColorTheme) {
                applyUpdate(state.copy(colorTheme = theme))
            }

            override fun updateWallpaper(wallpaper: WallpaperOption) {''', "controller color theme update")

theme = ROOT / "ui/theme/Theme.kt"
replace_once(theme,
'''    val colorScheme = if (prefs.highContrast) {
        baseScheme.copy(''',
'''    val palette = prefs.colorTheme
    val paletteScheme = baseScheme.copy(
        primary = if (isDark) palette.darkPrimary else palette.lightPrimary,
        onPrimary = if (isDark) palette.darkOnPrimary else palette.lightOnPrimary,
        primaryContainer = if (isDark) palette.darkContainer else palette.lightContainer,
        onPrimaryContainer = if (isDark) palette.darkOnContainer else palette.lightOnContainer,
        secondary = if (isDark) palette.darkSecondary else palette.lightSecondary
    )

    val colorScheme = if (prefs.highContrast) {
        paletteScheme.copy(''', "apply selected accent palette")
replace_once(theme,
'''    } else {
        baseScheme
    }

    val scale = prefs.textScale.scale''',
'''    } else {
        paletteScheme
    }

    val scale = prefs.textScale.scale''', "use selected palette scheme")

settings = ROOT / "ui/components/ThemeSettingsSheet.kt"
section = '''            // SECTION 2: ACCENT COLOUR PALETTE
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text(
                    text = "Accent Colour",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.SemiBold,
                    color = MaterialTheme.colorScheme.primary
                )
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                    contentPadding = PaddingValues(vertical = 4.dp)
                ) {
                    items(AppColorTheme.entries) { palette ->
                        val selected = prefs.colorTheme == palette
                        Column(
                            modifier = Modifier
                                .width(76.dp)
                                .clip(RoundedCornerShape(14.dp))
                                .clickable { controller.updateColorTheme(palette) }
                                .border(
                                    width = if (selected) 2.dp else 1.dp,
                                    color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant,
                                    shape = RoundedCornerShape(14.dp)
                                )
                                .padding(vertical = 10.dp, horizontal = 6.dp)
                                .semantics { contentDescription = "Select ${palette.label} accent colour" },
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(28.dp)
                                    .clip(CircleShape)
                                    .background(palette.swatch),
                                contentAlignment = Alignment.Center
                            ) {
                                if (selected) {
                                    Icon(
                                        imageVector = Icons.Default.Check,
                                        contentDescription = null,
                                        tint = Color.White,
                                        modifier = Modifier.size(16.dp)
                                    )
                                }
                            }
                            Text(
                                text = palette.label,
                                style = MaterialTheme.typography.labelSmall,
                                color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface,
                                fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
                                maxLines = 1
                            )
                        }
                    }
                }
            }

'''
replace_once(settings, "            // SECTION 2: WALLPAPER OPTIONS", section + "            // SECTION 3: WALLPAPER OPTIONS", "insert accent palette selector")
text = settings.read_text(encoding="utf-8")
text = text.replace("// SECTION 3: ACCESSIBILITY & VISUAL LEGIBILITY", "// SECTION 4: ACCESSIBILITY & VISUAL LEGIBILITY", 1)
settings.write_text(text, encoding="utf-8")

# Keep the previously deferred in-app updater out of this release.
for relative in ("ui/components/AppUpdateDialog.kt", "update/AppUpdater.kt"):
    target = ROOT / relative
    if target.exists():
        target.unlink()

print("Added persistent Light Blue, Ocean, Violet, Emerald and Rose accent palettes with live Settings selection")
