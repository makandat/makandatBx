USE user
CREATE TABLE `Pictures` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TITLE` varchar(50) NOT NULL,
  `CREATOR` varchar(50) NOT NULL,
  `PATH` varchar(500) NOT NULL,
  `MARK` varchar(10) DEFAULT NULL,
  `INFO` varchar(100) DEFAULT NULL,
  `FAV` char(1) DEFAULT '0',
  `COUNT` int(8) DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=279 DEFAULT CHARSET=utf8;

