package com.unina.osintcollector.controller;

import org.springframework.web.bind.annotation.*;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

@RestController
public class ProxyController {

    @RequestMapping("/proxy")
    public String proxyGoogleCSE(@RequestParam String param, String page) throws IOException {
        String encodedParam = URLEncoder.encode(param, StandardCharsets.UTF_8);

        URL url = new URL("https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=en&source=gcsc&gss=.io&start=" + page + "&cselibv=8435450f13508ca1&cx=006249643689853114236%3Aa3iibfpwexa&q=" + encodedParam + "&safe=off&cse_tok=AB-tC_59DoiauQdHWNJNzoowt1m3%3A1709059422192&sort=&exp=cc%2Cdtsq-3&fexp=72497452&callback=google.search.cse.api10114");

        HttpURLConnection http = (HttpURLConnection) url.openConnection();

        StringBuilder responseBody = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(http.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                responseBody.append(line);
            }
        } catch (IOException e) {
            //
        } finally {
            http.disconnect();
        }

        return extractJson(responseBody.toString());
    }


    private String extractJson(String responseBody) {
        int startIndex = responseBody.indexOf('{');
        int endIndex = responseBody.lastIndexOf('}');
        if (startIndex != -1 && endIndex != -1) {
            return responseBody.substring(startIndex, endIndex + 1);
        } else {
            //
            return "";
        }
    }

}
