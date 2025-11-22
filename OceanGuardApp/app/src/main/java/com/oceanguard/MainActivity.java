package com.oceanguard.app;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebSettings;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends Activity {

    private WebView webView;
    private EditText serverUrlInput;
    private Button connectButton;
    private Button refreshButton;

    // Default server URL (can be changed by user)
    private String serverUrl = "http://192.168.43.1:8000/gallery/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize views
        webView = findViewById(R.id.webView);
        serverUrlInput = findViewById(R.id.serverUrlInput);
        connectButton = findViewById(R.id.connectButton);
        refreshButton = findViewById(R.id.refreshButton);

        // Set default URL in input
        serverUrlInput.setText(serverUrl);

        // Configure WebView
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setUseWideViewPort(true);
        webSettings.setCacheMode(WebSettings.LOAD_NO_CACHE);

        // Handle links within WebView
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                Toast.makeText(MainActivity.this,
                    "Error: Cannot connect to server. Check WiFi and server URL.",
                    Toast.LENGTH_LONG).show();
            }
        });

        // Connect button click
        connectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                serverUrl = serverUrlInput.getText().toString();
                if (!serverUrl.startsWith("http://") && !serverUrl.startsWith("https://")) {
                    serverUrl = "http://" + serverUrl;
                }
                loadGallery();
            }
        });

        // Refresh button click
        refreshButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                webView.reload();
                Toast.makeText(MainActivity.this, "Refreshing gallery...", Toast.LENGTH_SHORT).show();
            }
        });

        // Load gallery on start
        loadGallery();
    }

    private void loadGallery() {
        Toast.makeText(this, "Connecting to OceanGuard Server...", Toast.LENGTH_SHORT).show();
        webView.loadUrl(serverUrl);
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
