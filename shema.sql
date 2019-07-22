CREATE TABLE `users` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`f_name` TINYTEXT NOT NULL,
	`l_name` TINYTEXT NULL,
	`tg_id` INT(10) UNSIGNED NOT NULL,
	`reg_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `tg_id` (`tg_id`)
);

CREATE TABLE `events` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`name` TINYTEXT NOT NULL,
	`about` TEXT NOT NULL,
	`creation_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
);

CREATE TABLE `tickets` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`user_id` INT(11) NULL DEFAULT NULL,
	`event_id` INT(11) NOT NULL,
	`change_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`creation_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
	`place` INT(10) UNSIGNED NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `user_id` (`user_id`),
	INDEX `event_id` (`event_id`),
	CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
);
