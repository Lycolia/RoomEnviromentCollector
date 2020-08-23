-- RoomEnviroments definition
CREATE TABLE `RoomEnviroments` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `temputure` float DEFAULT NULL,
  `humidity` float DEFAULT NULL,
  `createAt` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_createAt` (`createAt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Logs definition
CREATE TABLE `Logs` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `logFrom` varchar(256) NOT NULL,
  `level` tinyint(3) unsigned NOT NULL,
  `subject` varchar(128) DEFAULT NULL,
  `detail` varchar(2048) NOT NULL,
  `createAt` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `level_to_logs` (`level`),
  KEY `logFrom` (`logFrom`,`level`,`subject`),
  CONSTRAINT `level_to_logs` FOREIGN KEY (`level`) REFERENCES `LogLevel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;

-- LogLevel definition
CREATE TABLE `LogLevel` (
  `id` tinyint(3) unsigned NOT NULL,
  `name` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO LogLevel (id, name) VALUES(1, 'Info');
INSERT INTO LogLevel (id, name) VALUES(2, 'Warn');
INSERT INTO LogLevel (id, name) VALUES(3, 'Error');
INSERT INTO LogLevel (id, name) VALUES(4, 'Fatal');
INSERT INTO LogLevel (id, name) VALUES(5, 'Debug');
