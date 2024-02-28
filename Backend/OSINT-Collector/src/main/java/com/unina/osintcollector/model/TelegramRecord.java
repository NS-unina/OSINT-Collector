package com.unina.osintcollector.model;

public record TelegramRecord(TelegramMessage[] messages, TelegramGroup channel, TelegramUser[] users) {
}
