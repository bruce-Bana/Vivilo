package com.vivilo.media.update

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.core.content.FileProvider
import com.vivilo.media.BuildConfig
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.BufferedInputStream
import java.io.File
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL
import java.security.MessageDigest

private const val RELEASE_API = "https://api.github.com/repos/bruce-Bana/Vivilo/releases/latest"
private const val MAX_APK_BYTES = 250L * 1024L * 1024L

data class ViviloUpdate(
    val versionCode: Int,
    val versionName: String,
    val apkUrl: String,
    val checksumUrl: String,
    val releaseNotes: String
)

sealed interface UpdateCheckResult {
    data class Available(val update: ViviloUpdate) : UpdateCheckResult
    data object UpToDate : UpdateCheckResult
}

sealed interface InstallResult {
    data object InstallerOpened : InstallResult
    data object PermissionRequired : InstallResult
}

object AppUpdater {
    suspend fun checkForUpdate(): UpdateCheckResult = withContext(Dispatchers.IO) {
        val release = JSONObject(readText(RELEASE_API))
        val assets = release.getJSONArray("assets")
        var apkUrl: String? = null
        var checksumUrl: String? = null
        var versionUrl: String? = null
        for (i in 0 until assets.length()) {
            val asset = assets.getJSONObject(i)
            when (asset.optString("name")) {
                "vivilo.apk" -> apkUrl = asset.optString("browser_download_url")
                "vivilo.apk.sha256" -> checksumUrl = asset.optString("browser_download_url")
                "vivilo-version.json" -> versionUrl = asset.optString("browser_download_url")
            }
        }
        val version = JSONObject(readText(versionUrl ?: error("The latest release has no version manifest")))
        val remoteCode = version.getInt("versionCode")
        if (remoteCode <= BuildConfig.VERSION_CODE) return@withContext UpdateCheckResult.UpToDate
        UpdateCheckResult.Available(
            ViviloUpdate(
                versionCode = remoteCode,
                versionName = version.getString("versionName"),
                apkUrl = apkUrl ?: error("The release is missing vivilo.apk"),
                checksumUrl = checksumUrl ?: error("The release is missing its SHA-256 checksum"),
                releaseNotes = release.optString("body", "")
            )
        )
    }

    suspend fun downloadAndInstall(activity: Activity, update: ViviloUpdate): InstallResult =
        withContext(Dispatchers.IO) {
            val folder = File(activity.cacheDir, "updates").apply { mkdirs() }
            val apkFile = File(folder, "vivilo-${update.versionCode}.apk")
            val connection = openConnection(update.apkUrl)
            try {
                require(connection.contentLengthLong <= MAX_APK_BYTES) { "Update file is unexpectedly large" }
                BufferedInputStream(connection.inputStream).use { input ->
                    FileOutputStream(apkFile).use { output ->
                        val buffer = ByteArray(32 * 1024)
                        var total = 0L
                        while (true) {
                            val count = input.read(buffer)
                            if (count < 0) break
                            total += count
                            require(total <= MAX_APK_BYTES) { "Update file exceeded the size limit" }
                            output.write(buffer, 0, count)
                        }
                        output.fd.sync()
                    }
                }
            } finally {
                connection.disconnect()
            }

            val expected = readText(update.checksumUrl).trim()
                .substringBefore(" ").substringBefore("\t").lowercase()
            require(expected.matches(Regex("[a-f0-9]{64}"))) { "Release checksum is invalid" }
            val digest = MessageDigest.getInstance("SHA-256")
            apkFile.inputStream().buffered().use { input ->
                val buffer = ByteArray(32 * 1024)
                while (true) {
                    val count = input.read(buffer)
                    if (count < 0) break
                    digest.update(buffer, 0, count)
                }
            }
            val actual = digest.digest().joinToString("") { "%02x".format(it) }
            require(actual == expected) { "APK checksum verification failed; installation was stopped" }

            withContext(Dispatchers.Main) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O &&
                    !activity.packageManager.canRequestPackageInstalls()
                ) {
                    activity.startActivity(
                        Intent(
                            Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                            Uri.parse("package:${activity.packageName}")
                        )
                    )
                    InstallResult.PermissionRequired
                } else {
                    val uri = FileProvider.getUriForFile(
                        activity,
                        "${activity.packageName}.fileprovider",
                        apkFile
                    )
                    activity.startActivity(
                        Intent(Intent.ACTION_VIEW).apply {
                            setDataAndType(uri, "application/vnd.android.package-archive")
                            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                        }
                    )
                    InstallResult.InstallerOpened
                }
            }
        }

    private fun readText(url: String): String {
        val connection = openConnection(url)
        return try {
            connection.inputStream.bufferedReader(Charsets.UTF_8).use { it.readText() }
        } finally {
            connection.disconnect()
        }
    }

    private fun openConnection(url: String): HttpURLConnection {
        require(url.startsWith("https://")) { "Updates must use HTTPS" }
        return (URL(url).openConnection() as HttpURLConnection).apply {
            connectTimeout = 15_000
            readTimeout = 30_000
            instanceFollowRedirects = true
            setRequestProperty("User-Agent", "Vivilo-Android/${BuildConfig.VERSION_NAME}")
            setRequestProperty("Accept", "application/vnd.github+json")
            connect()
            if (responseCode !in 200..299) {
                val code = responseCode
                disconnect()
                error("GitHub returned HTTP $code while checking for updates")
            }
        }
    }
}
