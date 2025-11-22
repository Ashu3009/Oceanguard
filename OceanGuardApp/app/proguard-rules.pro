# Add project specific ProGuard rules here.
-keep class com.oceanguard.app.** { *; }
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
