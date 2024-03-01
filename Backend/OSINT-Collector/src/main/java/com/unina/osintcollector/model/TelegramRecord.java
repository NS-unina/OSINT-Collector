package com.unina.osintcollector.model;

public record TelegramRecord(TelegramMessage[] msgs, TelegramGroup channel, TelegramUser[] users) {
}
