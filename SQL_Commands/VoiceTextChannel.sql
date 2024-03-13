-- SQLite
CREATE TABLE IF NOT EXISTS `VoiceTextChannel` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `text_channel_id` TEXT NOT NULL,
    `voice_channel_id` TEXT NOT NULL
);