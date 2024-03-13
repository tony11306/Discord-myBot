-- SQLite
CREATE TABLE IF NOT EXISTS `Remind` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `time` TEXT NOT NULL,
    `title` TEXT NOT NULL,
    `is_private` INTEGER NOT NULL,
    `user_id` TEXT NOT NULL,
    `server_id` TEXT NOT NULL,
    FOREIGN KEY(`server_id`) REFERENCES `ServerRemindChat`(`server_id`) ON DELETE CASCADE
);