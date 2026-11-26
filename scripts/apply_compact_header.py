from pathlib import Path

ROOT = Path("source/app/src/main/java/com/vivilo/media/ui/screens")
components = ROOT / "BrowserComponents.kt"

def one(path, old, new, label):
    data = path.read_text(encoding="utf-8")
    count = data.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, found {count}")
    path.write_text(data.replace(old, new, 1), encoding="utf-8")

# Active search header: reduce its vertical footprint and control hitboxes without
# compromising accessibility or the text field's focus/IME behaviour.
one(components,
'''                .padding(horizontal = 12.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)''',
'''                .padding(horizontal = 12.dp, vertical = 4.dp),
            verticalArrangement = Arrangement.spacedBy(4.dp)''',
"active search header spacing")
one(components, '.height(52.dp)', '.height(42.dp)', "active search field height")
one(components, 'shadowElevation = 6.dp,', 'shadowElevation = 3.dp,', "active search field elevation")
one(components, '.size(48.dp)\n                            .testTag("top_bar_back_button")', '.size(40.dp)\n                            .testTag("top_bar_back_button")', "back control size")
one(components, '.size(48.dp)\n                                    .testTag("clear_search_button")', '.size(40.dp)\n                                    .testTag("clear_search_button")', "clear search control size")
one(components, '.size(48.dp)\n                        .testTag("toggle_view_mode_button")', '.size(40.dp)\n                        .testTag("toggle_view_mode_button")', "view toggle size")

# Home header: compact brand row, actions and search launcher.
one(components,
'''            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)''',
'''            .padding(horizontal = 16.dp, vertical = 4.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp)''',
"home header spacing")
one(components, '.size(48.dp)\n                        .testTag("refresh_library_button")', '.size(40.dp)\n                        .testTag("refresh_library_button")', "refresh control size")
one(components, '.size(48.dp)\n                        .testTag("theme_settings_button")', '.size(40.dp)\n                        .testTag("theme_settings_button")', "settings control size")
one(components, 'modifier = Modifier.size(24.dp),\n                        tint = MaterialTheme.colorScheme.primary\n                    )\n                }\n                IconButton(\n                    onClick = onOpenSettings', 'modifier = Modifier.size(20.dp),\n                        tint = MaterialTheme.colorScheme.primary\n                    )\n                }\n                IconButton(\n                    onClick = onOpenSettings', "refresh icon size")
one(components, 'modifier = Modifier.size(26.dp),\n                        tint = MaterialTheme.colorScheme.primary\n                    )\n                }\n            }\n        }\n\n        Surface(', 'modifier = Modifier.size(20.dp),\n                        tint = MaterialTheme.colorScheme.primary\n                    )\n                }\n            }\n        }\n\n        Surface(', "settings icon size")
one(components, '.height(54.dp)\n                .clickable { onSearchOpen() }', '.height(42.dp)\n                .clickable { onSearchOpen() }', "home search launcher height")
one(components, '.padding(start = 18.dp, end = 6.dp),\n                verticalAlignment = Alignment.CenterVertically,\n                horizontalArrangement = Arrangement.spacedBy(10.dp)', '.padding(start = 14.dp, end = 6.dp),\n                verticalAlignment = Alignment.CenterVertically,\n                horizontalArrangement = Arrangement.spacedBy(8.dp)', "home search inner spacing")
one(components, 'modifier = Modifier.size(22.dp)\n                )\n                // Display-only', 'modifier = Modifier.size(18.dp)\n                )\n                // Display-only', "home search icon size")

# Category chips: shave vertical padding, height and horizontal padding.
one(components,
'''        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)''',
'''        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 4.dp),
        horizontalArrangement = Arrangement.spacedBy(6.dp)''',
"category row padding")
one(components, '.height(40.dp)\n                    .testTag("filter_tab_', '.height(34.dp)\n                    .testTag("filter_tab_', "category chip height")
one(components, 'modifier = Modifier.padding(horizontal = 14.dp),\n                    verticalAlignment = Alignment.CenterVertically,\n                    horizontalArrangement = Arrangement.spacedBy(6.dp)', 'modifier = Modifier.padding(horizontal = 10.dp),\n                    verticalAlignment = Alignment.CenterVertically,\n                    horizontalArrangement = Arrangement.spacedBy(5.dp)', "category chip padding")
one(components, 'modifier = Modifier.size(18.dp),\n                        tint = if (isSelected)', 'modifier = Modifier.size(16.dp),\n                        tint = if (isSelected)', "category icon size")

# Compact the brand lockup without changing the app identity.
logo = Path("source/app/src/main/java/com/vivilo/media/ui/components/CoolViviloLogo.kt")
one(logo, 'horizontalArrangement = Arrangement.spacedBy(10.dp)\n    ) {\n        CoolViviloLogo(size = 40.dp)', 'horizontalArrangement = Arrangement.spacedBy(8.dp)\n    ) {\n        CoolViviloLogo(size = 30.dp)', "brand logo size")
one(logo, 'style = MaterialTheme.typography.titleLarge,\n                    fontWeight = FontWeight.Bold,', 'style = MaterialTheme.typography.titleMedium,\n                    fontWeight = FontWeight.Bold,', "brand title size")
one(logo, 'text = "Media player & file manager",', 'text = "Media & files",', "brand tagline length")

print("Compacted home header, search controls, category filters and brand lockup")
