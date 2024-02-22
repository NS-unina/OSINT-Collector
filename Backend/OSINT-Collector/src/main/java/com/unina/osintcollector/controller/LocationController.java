package com.unina.osintcollector.controller;

import com.unina.osintcollector.model.Category;
import com.unina.osintcollector.model.Location;
import com.unina.osintcollector.repository.LocationRepository;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/locations")
public class LocationController {

    private final LocationRepository locationRepository;

    public LocationController(LocationRepository locationRepository) {
        this.locationRepository = locationRepository;
    }

    @GetMapping(value = { "/", "" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public Flux<Location> getLocations() {
        return locationRepository.findAll();
    }
}
