from pathlib import Path
import shutil

root = Path("source")
def patch(path, old, new, label):
    p = root / path
    s = p.read_text(encoding="utf-8")
    if new in s:
        return
    if old not in s:
        raise SystemExit(f"Could not patch {label}: expected source text not found")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")

patch(
    "app/build.gradle.kts",
    '    versionCode = 1\n    versionName = "1.0.0"',
    '    versionCode = providers.environmentVariable("VIVILO_VERSION_CODE").orNull?.toIntOrNull() ?: 1\n    versionName = providers.environmentVariable("VIVILO_VERSION_NAME").orNull ?: "1.0.0"',
    "version metadata"
)
manifest = root / "app/src/main/AndroidManifest.xml"
m = manifest.read_text(encoding="utf-8")
if "android.permission.INTERNET" not in m:
    m = m.replace(
        '<manifest xmlns:android="http://schemas.android.com/apk/res/android">',
        '<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n\n    <uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />',
        1
    )
manifest.write_text(m, encoding="utf-8")

paths = root / "app/src/main/res/xml/file_paths.xml"
p = paths.read_text(encoding="utf-8")
if '<cache-path name="updates"' not in p:
    paths.write_text(p.replace("</paths>", '    <cache-path name="updates" path="updates/" />\n</paths>'), encoding="utf-8")

for relative in (
    "app/src/main/java/com/vivilo/media/update/AppUpdater.kt",
    "app/src/main/java/com/vivilo/media/ui/components/AppUpdateDialog.kt",
):
    source_file = Path(relative)
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_file, target)

components = root / "app/src/main/java/com/vivilo/media/ui/screens/BrowserComponents.kt"
c = components.read_text(encoding="utf-8")
if "import androidx.compose.material.icons.filled.SystemUpdateAlt" not in c:
    c = c.replace(
        "import androidx.compose.material.icons.filled.Storage",
        "import androidx.compose.material.icons.filled.Storage\nimport androidx.compose.material.icons.filled.SystemUpdateAlt",
        1
    )
c = c.replace(
    "    onOpenSettings: () -> Unit = {}\n)",
    "    onOpenSettings: () -> Unit = {},\n    onCheckUpdates: () -> Unit = {}\n)",
    1
)
needle = '''                IconButton(
                    onClick = onOpenSettings,
                    modifier = Modifier
                        .size(48.dp)
                        .testTag("theme_settings_button")
                ) {'''
insert = '''                IconButton(
                    onClick = onCheckUpdates,
                    modifier = Modifier
                        .size(48.dp)
                        .testTag("check_updates_button")
                ) {
                    Icon(
                        imageVector = Icons.Default.SystemUpdateAlt,
                        contentDescription = "Check for app updates",
                        modifier = Modifier.size(24.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                }
                IconButton(
                    onClick = onOpenSettings,
                    modifier = Modifier
                        .size(48.dp)
                        .testTag("theme_settings_button")
                ) {'''
if "onCheckUpdates: () -> Unit" not in c:
    if needle not in c:
        raise SystemExit("Could not add update button to the home header")
    c = c.replace(needle, insert, 1)
components.write_text(c, encoding="utf-8")

browser = root / "app/src/main/java/com/vivilo/media/ui/screens/BrowserScreen.kt"
b = browser.read_text(encoding="utf-8")
if "import com.vivilo.media.ui.components.AppUpdateDialog" not in b:
    b = b.replace(
        "import com.vivilo.media.ui.components.ThemeSettingsSheet",
        "import com.vivilo.media.ui.components.AppUpdateDialog\nimport com.vivilo.media.ui.components.ThemeSettingsSheet",
        1
    )
if "var showAppUpdateDialog" not in b:
    b = b.replace(
        "    var showThemeSettings by remember { mutableStateOf(false) }",
        "    var showThemeSettings by remember { mutableStateOf(false) }\n    var showAppUpdateDialog by remember { mutableStateOf(false) }",
        1
    )
if "AppUpdateDialog(onDismiss" not in b:
    b = b.replace(
        '''    if (showThemeSettings) {
        ThemeSettingsSheet(
            onDismissRequest = { showThemeSettings = false }
        )
    }
''',
        '''    if (showThemeSettings) {
        ThemeSettingsSheet(
            onDismissRequest = { showThemeSettings = false }
        )
    }
    if (showAppUpdateDialog) {
        AppUpdateDialog(onDismiss = { showAppUpdateDialog = false })
    }
''',
        1
    )
if "onCheckUpdates = { showAppUpdateDialog = true }" not in b:
    b = b.replace(
        "                                onOpenSettings = { showThemeSettings = true }\n",
        "                                onOpenSettings = { showThemeSettings = true },\n                                onCheckUpdates = { showAppUpdateDialog = true }\n",
        1
    )
browser.write_text(b, encoding="utf-8")
print("Installed update manager, app versioning, INTERNET/install permissions, checksum verification and update UI.")
