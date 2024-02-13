package com.unina.osintcollector.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;

@Controller
public class ImageController {

    @Autowired
    private RestTemplate restTemplate;

    @GetMapping("/proxy-image")
    @ResponseBody
    public ResponseEntity<byte[]> proxyImage(@RequestParam String url) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.set(HttpHeaders.USER_AGENT, "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)"); // Set your user agent here
            ResponseEntity<byte[]> responseEntity = restTemplate.exchange(url, HttpMethod.GET, new HttpEntity<>(headers), byte[].class);
            return ResponseEntity.status(responseEntity.getStatusCode()).contentType(MediaType.IMAGE_JPEG).body(responseEntity.getBody());
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }
}