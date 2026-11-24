package com.vivilo.media.ui.components

import android.app.Activity
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CloudDownload
import androidx.compose.material.icons.filled.SystemUpdateAlt
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.vivilo.media.BuildConfig
import com.vivilo.media.update.AppUpdater
import com.vivilo.media.update.InstallResult
import com.vivilo.media.update.UpdateCheckResult
import com.vivilo.media.update.ViviloUpdate
import kotlinx.coroutines.launch

@Composable
fun AppUpdateDialog(onDismiss: () -> Unit) {
    val activity = LocalContext.current as? Activity
    val scope = rememberCoroutineScope()
    var update by remember { mutableStateOf<ViviloUpdate?>(null) }
    var status by remember { mutableStateOf("Checking the official Vivilo release...") }
    var checking by remember { mutableStateOf(true) }
    var downloading by remember { mutableStateOf(false) }

    fun check() {
        checking = true
        status = "Checking the official Vivilo release..."
        scope.launch {
            runCatching { AppUpdater.checkForUpdate() }
                .onSuccess { result ->
                    update = (result as? UpdateCheckResult.Available)?.update
                    status = if (result is UpdateCheckResult.UpToDate) {
                        "You're up to date. Vivilo \${BuildConfig.VERSION_NAME} is the latest version."
                    } else {
                        "Version \${update?.versionName} is available."
                    }
                }
                .onFailure { status = "Update check failed: \${it.message ?: "Please try again."}" }
            checking = false
        }
    }

    LaunchedEffect(Unit) { check() }

    AlertDialog(
        onDismissRequest = { if (!checking && !downloading) onDismiss() },
        icon = { Icon(Icons.Default.SystemUpdateAlt, contentDescription = null) },
        title = { Text("Vivilo updates", fontWeight = FontWeight.Bold) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("Installed: \${BuildConfig.VERSION_NAME} (build \${BuildConfig.VERSION_CODE})")
                Text(status, style = MaterialTheme.typography.bodyMedium)
                update?.let {
                    Text("Available: \${it.versionName} (build \${it.versionCode})", fontWeight = FontWeight.SemiBold)
                    if (it.releaseNotes.isNotBlank()) {
                        Text(
                            it.releaseNotes.take(500),
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
                if (checking || downloading) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        CircularProgressIndicator(strokeWidth = 2.dp)
                        Spacer(Modifier.width(10.dp))
                        Text(if (checking) "Checking releases..." else "Downloading and verifying APK...")
                    }
                }
                Text(
                    "Downloads come from the official GitHub release and are SHA-256 checked. Android will ask you to confirm installation.",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        },
        confirmButton = {
            if (update == null) {
                TextButton(onClick = { check() }, enabled = !checking) { Text("Check again") }
            } else {
                Button(
                    enabled = !checking && !downloading && activity != null,
                    onClick = {
                        val selected = update ?: return@Button
                        downloading = true
                        status = "Downloading update and verifying its checksum..."
                        scope.launch {
                            runCatching { AppUpdater.downloadAndInstall(activity!!, selected) }
                                .onSuccess { result ->
                                    status = if (result == InstallResult.PermissionRequired) {
                                        "Allow Vivilo to install unknown apps in Android settings, return here, then tap Install update again."
                                    } else {
                                        "Verified APK sent to Android's installer. Follow the system prompts."
                                    }
                                }
                                .onFailure { status = "Update failed: \${it.message ?: "Please try again."}" }
                            downloading = false
                        }
                    }
                ) {
                    Icon(Icons.Default.CloudDownload, contentDescription = null)
                    Spacer(Modifier.width(6.dp))
                    Text("Install update")
                }
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss, enabled = !checking && !downloading) { Text("Close") }
        }
    )
}
