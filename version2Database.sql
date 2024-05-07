-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: waste_management
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('0caadfde629f');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `DID` int NOT NULL AUTO_INCREMENT,
  `departmentName` varchar(200) NOT NULL,
  `departmentType` enum('METALLURGY','EQUIPMENT_MANUFACTURING','COMPOSITE_MATERIAL','NEW_ENERGY','AUTOMATION_SYSTEM','MAINTENANCE','LABORATORY','DATA_CENTER','OFFICE') NOT NULL,
  `departmentAddress` varchar(500) NOT NULL,
  PRIMARY KEY (`DID`),
  UNIQUE KEY `departmentName` (`departmentName`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'Advanced Metallurgy Division','METALLURGY','101 Steel Avenue'),(2,'High-End Equipment Manufacturing Co.','EQUIPMENT_MANUFACTURING','202 Precision Road'),(3,'Composite Materials Innovations LLC','COMPOSITE_MATERIAL','303 Composite Loop'),(4,'Green Energy Solutions','NEW_ENERGY','404 Sustainable Way'),(5,'Automation Systems Corp.','AUTOMATION_SYSTEM','505 Automation Alley'),(6,'Equipment Maintenance and Services','MAINTENANCE','606 Maintenance Drive'),(7,'Advanced Research Labs','LABORATORY','707 Innovation Blvd'),(8,'Central Data Center','DATA_CENTER','808 Data Stream Road'),(9,'Corporate Headquarters','OFFICE','909 Executive Row');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `OID` int NOT NULL AUTO_INCREMENT,
  `UID` int DEFAULT NULL,
  `date` date NOT NULL,
  `finishDate` date DEFAULT NULL,
  `orderName` varchar(300) NOT NULL,
  `wasteType` enum('HEAVY_METAL_WASTEWATER','EXHAUST_GAS','MINERAL_RESIDUE','CUTTING_FLUID','METAL_CHIPS','PLASTIC','COMPOSITE_MATERIAL_CUTTING_WASTE','WASTE_PAINT','DUST','CHEMICALS','CATALYZER','CHEMICAL_PROPELLANTS','FUEL_RESIDUES','DISCARDED_ELECTRONIC_COMPONENTS','HYDRAULIC_OIL','LUBRICANT_WASTE','HAZARDOUS_CHEMICALS','WASTE_EXPERIMENTAL_EQUIPMENT','WASTE_HEAT','WASTE_PAPER','HOUSEHOLD_WASTE') NOT NULL,
  `weight` int NOT NULL,
  `attribution` text NOT NULL,
  `multiplier` float NOT NULL,
  `comment` text,
  `orderStatus` enum('UNCONFIRMED','CONFIRM','PROCESSING','FINISHED','DISCHARGED') NOT NULL,
  `department_id` int DEFAULT NULL,
  PRIMARY KEY (`OID`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `department` (`DID`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,1,'2024-04-19',NULL,'Metal Wastewater Disposal','HEAVY_METAL_WASTEWATER',500,'CuSo4:10%',1.9,'Metal Wastewater Disposal','PROCESSING',1),(2,1,'2024-04-17',NULL,'Exhaust Gas Treatment','EXHAUST_GAS',20,'So2:10%',1,'Exhaust Gas Treatment','PROCESSING',1),(3,2,'2024-04-16',NULL,'Cutting Fluid Recycling','CUTTING_FLUID',15,'waste oil:100%',1.3,'Cutting Fluid Recycling','CONFIRM',2),(4,2,'2024-04-15',NULL,'Plastic Waste Management','PLASTIC',80,'PVC:100%',1,'Plastic Waste Management','CONFIRM',2),(5,3,'2024-04-05',NULL,'Chemical Propellant Disposal','CHEMICALS',40,'C2H2:20%',1,'Chemical Propellant Disposal','CONFIRM',3),(6,2,'2024-04-09',NULL,'Waste Paint Disposal','WASTE_PAINT',25,'Lead paint:70%',1,'Waste Paint Disposal','CONFIRM',2),(7,3,'2024-04-01',NULL,'Industrial Dust Collection','DUST',150,'Industrial dust:95%',1,'Industrial Dust Collection','UNCONFIRMED',3),(8,3,'2024-03-19',NULL,'Chemical Waste Handling','CHEMICALS',80,'Acetic acid:20%',1,'Chemical Waste Handling','UNCONFIRMED',3),(9,3,'2024-01-19',NULL,'Catalyzer Recycling','CATALYZER',10,'Used nickel:30%',1,'Catalyzer Recycling','UNCONFIRMED',3),(10,4,'2024-04-16',NULL,'Chemical Propellants Disposal','CHEMICAL_PROPELLANTS',40,'Rocket fuel:50%',1,'Chemical Propellants Disposal','UNCONFIRMED',4),(11,4,'2024-04-15',NULL,'Fuel Residue Processing','FUEL_RESIDUES',60,'Oil sludge:75%',1,'Fuel Residue Processing','UNCONFIRMED',4),(12,5,'2024-04-11',NULL,'Electronic Components Recycling','DISCARDED_ELECTRONIC_COMPONENTS',90,'Obsolete ICs:40%',1,'Electronic Components Recycling','UNCONFIRMED',5),(13,6,'2024-04-18',NULL,'Hydraulic Oil Recycling','HYDRAULIC_OIL',70,'Used hydraulic fluid:80%',1,'Hydraulic Oil Recycling','UNCONFIRMED',6),(14,6,'2024-04-15',NULL,'Lubricant Waste Collection','LUBRICANT_WASTE',45,'Engine grease:60%',1,'Lubricant Waste Collection','UNCONFIRMED',6),(15,7,'2024-04-03',NULL,'Hazardous Chemical Disposal','HAZARDOUS_CHEMICALS',50,'Toxic reagents:30%',1,'Hazardous Chemical Disposal','UNCONFIRMED',7),(16,7,'2023-05-25',NULL,'Experimental Equipment Clearance','WASTE_EXPERIMENTAL_EQUIPMENT',20,'Broken pipettes:100%',1,'Experimental Equipment Clearance','UNCONFIRMED',7),(17,8,'2023-05-27',NULL,'Waste Heat Utilization','WASTE_HEAT',200,'Industrial heat:90%',1,'Waste Heat Utilization','UNCONFIRMED',8),(18,9,'2023-05-29',NULL,'Paper Recycling','WASTE_PAPER',150,'Office paper:50%',1,'Paper Recycling','UNCONFIRMED',9),(19,9,'2023-05-31',NULL,'Household Waste Segregation','HOUSEHOLD_WASTE',180,'Kitchen waste:40%',1,'Household Waste Segregation','UNCONFIRMED',9),(20,2,'2023-06-02',NULL,'Metal Chips Processing','METAL_CHIPS',85,'Aluminum chips:70%',1,'Metal Chips Processing','UNCONFIRMED',2),(21,1,'2023-06-04',NULL,'Mineral Residue Processing','MINERAL_RESIDUE',60,'Tailings:95%',1,'Mineral Residue Processing','UNCONFIRMED',1),(22,3,'2023-06-06',NULL,'Composite Material Cutting Disposal','COMPOSITE_MATERIAL_CUTTING_WASTE',30,'Carbon fiber:60%',1,'Composite Material Cutting Disposal','UNCONFIRMED',3),(23,4,'2023-06-08',NULL,'Fuel Residue Processing','FUEL_RESIDUES',65,'Oil sludge:80%',1,'Fuel Residue Processing','UNCONFIRMED',4),(24,5,'2023-06-10',NULL,'Electronic Components Recycling','DISCARDED_ELECTRONIC_COMPONENTS',95,'Obsolete ICs:45%',1,'Electronic Components Recycling','UNCONFIRMED',5),(25,6,'2023-06-12',NULL,'Lubricant Waste Collection','LUBRICANT_WASTE',50,'Engine grease:65%',1,'Lubricant Waste Collection','UNCONFIRMED',6),(26,7,'2023-06-14',NULL,'Hazardous Chemical Disposal','HAZARDOUS_CHEMICALS',55,'Toxic reagents:35%',1,'Hazardous Chemical Disposal','UNCONFIRMED',7),(27,8,'2023-06-16',NULL,'Waste Heat Utilization','WASTE_HEAT',205,'Industrial heat:95%',1,'Waste Heat Utilization','UNCONFIRMED',8),(28,9,'2023-06-18',NULL,'Paper Recycling','WASTE_PAPER',155,'Office paper:55%',1,'Paper Recycling','UNCONFIRMED',9),(29,3,'2023-06-20',NULL,'Dust Collection from Cutting','DUST',160,'Wood dust:90%',1,'Dust Collection from Cutting','UNCONFIRMED',3),(30,6,'2023-06-22',NULL,'Hydraulic Oil Recycling','HYDRAULIC_OIL',75,'Used hydraulic fluid:85%',1,'Hydraulic Oil Recycling','UNCONFIRMED',6),(31,2,'2024-04-19',NULL,'Industrial Fluid Reuse','CUTTING_FLUID',14,'Recycled oil:95%',1,'Industrial Fluid Reuse','UNCONFIRMED',2),(32,2,'2024-04-18',NULL,'Synthetic Resin Disposal','PLASTIC',75,'Polyethylene:90%',18,'Synthetic Resin Disposal','CONFIRM',2),(33,2,'2024-04-17',NULL,'Eco Paint Collection','WASTE_PAINT',22,'Non-toxic paint:65%',1,'Eco Paint Collection','UNCONFIRMED',2),(34,2,'2024-04-19',NULL,'Iron Shavings Processing','METAL_CHIPS',80,'Iron chips:75%',1,'Iron Shavings Processing','PROCESSING',2),(36,2,'2024-04-19',NULL,'Composite Material Sorting','COMPOSITE_MATERIAL_CUTTING_WASTE',30,'Fiberglass waste:50%',1,'Composite Material Sorting','CONFIRM',2),(37,2,'2024-04-15',NULL,'Used Oil Filtration','CUTTING_FLUID',18,'Motor oil:88%',1,'Used Oil Filtration','UNCONFIRMED',2),(38,2,'2024-04-14',NULL,'Recycled Plastic Use','PLASTIC',78,'HDPE:80%',1,'Recycled Plastic Use','UNCONFIRMED',2),(39,2,'2024-04-16',NULL,'Paint Waste Processing','WASTE_PAINT',28,'Acrylic paint:60%',1,'Paint Waste Processing','UNCONFIRMED',2),(40,2,'2024-04-17',NULL,'Steel Chips Recycle','METAL_CHIPS',87,'Steel chips:80%',1,'Steel Chips Recycle','PROCESSING',2),(41,2,'2024-04-10',NULL,'Advanced Composite Disposal','COMPOSITE_MATERIAL_CUTTING_WASTE',33,'Carbon composite waste:55%',1,'Advanced Composite Disposal','UNCONFIRMED',2),(42,2,'2024-04-09',NULL,'Coolant Oil Recovery','CUTTING_FLUID',12,'Coolant mix:100%',1,'Coolant Oil Recovery','UNCONFIRMED',2),(43,2,'2024-04-12',NULL,'Plastic Scraps Handling','PLASTIC',82,'Polystyrene:70%',1,'Plastic Scraps Handling','UNCONFIRMED',2),(44,2,'2024-04-15',NULL,'Hazardous Paint Removal','WASTE_PAINT',30,'Chemical paint:75%',1,'Hazardous Paint Removal','UNCONFIRMED',2),(45,2,'2024-04-04',NULL,'Copper Filings Management','METAL_CHIPS',82,'Copper chips:68%',1,'Copper Filings Management','UNCONFIRMED',2),(46,2,'2024-04-06',NULL,'Composite Material Recycling','COMPOSITE_MATERIAL_CUTTING_WASTE',28,'Mixed composites waste:60%',1,'Composite Material Recycling','UNCONFIRMED',2),(47,2,'2024-04-19',NULL,'Engine Oil Recycling','CUTTING_FLUID',16,'Used engine oil:92%',1,'Engine Oil Recycling','CONFIRM',2),(48,2,'2024-04-16',NULL,'Biodegradable Plastic Sorting','PLASTIC',77,'Biodegradable plastic:85%',1,'Biodegradable Plastic Sorting','UNCONFIRMED',2),(49,2,'2024-04-13',NULL,'Ecological Paint Handling','WASTE_PAINT',26,'Water-based paint:77%',1,'Ecological Paint Handling','UNCONFIRMED',2),(50,2,'2024-04-19',NULL,'Zinc Chips Sorting','METAL_CHIPS',83,'Zinc chips:73%',1,'Zinc Chips Sorting','PROCESSING',2),(51,1,'2024-04-19',NULL,' Heavy Metal Sludge Management','HEAVY_METAL_WASTEWATER',521,'ZnCl2:8%',1,'Heavy Metal Sludge Management','UNCONFIRMED',1),(52,1,'2024-04-19',NULL,'Industrial Smoke Cleanup','EXHAUST_GAS',25,'NOx:12%',1,'Industrial Smoke Cleanup','CONFIRM',1),(53,1,'2024-04-19',NULL,'Ore Tailings Treatment','MINERAL_RESIDUE',55,'Rock dust:90%',1.8,'Ore Tailings Treatment','PROCESSING',1),(54,1,'2023-04-18',NULL,'Acidic Water Neutralization','HEAVY_METAL_WASTEWATER',510,'H2SO4:5%',1,'Acidic Water Neutralization','UNCONFIRMED',1),(55,1,'2024-04-11',NULL,'Vehicular Emissions Control','EXHAUST_GAS',23,'CO:15%',1,'Vehicular Emissions Control','UNCONFIRMED',1),(56,1,'2024-04-13',NULL,' Sand Waste Processing','MINERAL_RESIDUE',655,'Sand residue:88%',1,'Sand Waste Processing','UNCONFIRMED',1),(58,1,'2024-04-14',NULL,'Furnace Gas Treatment','EXHAUST_GAS',22,'HCl:9%',1,'Furnace Gas Treatment','CONFIRM',1),(59,1,'2024-04-17',NULL,'Clay Residue Handling','MINERAL_RESIDUE',58,'Clay particles:93%',1,'Clay Residue Handling','UNCONFIRMED',1),(60,1,'2024-04-19',NULL,' Lead Contaminated Water Cleanup','HEAVY_METAL_WASTEWATER',505,'Pb(NO3)2:6%',1,'Lead Contaminated Water Cleanup','UNCONFIRMED',1);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `processcapacity`
--

DROP TABLE IF EXISTS `processcapacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `processcapacity` (
  `PCID` int NOT NULL AUTO_INCREMENT,
  `wasteType` enum('HEAVY_METAL_WASTEWATER','EXHAUST_GAS','MINERAL_RESIDUE','CUTTING_FLUID','METAL_CHIPS','PLASTIC','COMPOSITE_MATERIAL_CUTTING_WASTE','WASTE_PAINT','DUST','CHEMICALS','CATALYZER','CHEMICAL_PROPELLANTS','FUEL_RESIDUES','DISCARDED_ELECTRONIC_COMPONENTS','HYDRAULIC_OIL','LUBRICANT_WASTE','HAZARDOUS_CHEMICALS','WASTE_EXPERIMENTAL_EQUIPMENT','WASTE_HEAT','WASTE_PAPER','HOUSEHOLD_WASTE') NOT NULL,
  `maxCapacity` float NOT NULL,
  `currentCapacity` float NOT NULL,
  PRIMARY KEY (`PCID`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processcapacity`
--

LOCK TABLES `processcapacity` WRITE;
/*!40000 ALTER TABLE `processcapacity` DISABLE KEYS */;
INSERT INTO `processcapacity` VALUES (1,'HEAVY_METAL_WASTEWATER',10000,950),(2,'EXHAUST_GAS',1000,20),(3,'MINERAL_RESIDUE',1000,99),(4,'CUTTING_FLUID',1000,0),(5,'METAL_CHIPS',1000,250),(6,'PLASTIC',1000,0),(7,'COMPOSITE_MATERIAL_CUTTING_WASTE',1000,0),(8,'WASTE_PAINT',1000,0),(9,'DUST',1000,0),(10,'CHEMICALS',1000,0),(11,'CATALYZER',1000,0),(12,'CHEMICAL_PROPELLANTS',1000,0),(13,'FUEL_RESIDUES',1000,0),(14,'DISCARDED_ELECTRONIC_COMPONENTS',1000,0),(15,'HYDRAULIC_OIL',1000,0),(16,'LUBRICANT_WASTE',1000,0),(17,'HAZARDOUS_CHEMICALS',1000,0),(18,'WASTE_EXPERIMENTAL_EQUIPMENT',1000,0),(19,'WASTE_HEAT',1000,0),(20,'WASTE_PAPER',1000,0),(21,'HOUSEHOLD_WASTE',1000,0);
/*!40000 ALTER TABLE `processcapacity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(256) NOT NULL,
  `email` varchar(100) NOT NULL,
  `status` enum('DEPARTMENT_MANAGER','WASTE_MANAGER','GOVERNMENT_MANAGER','INDIVIDUAL_USER') NOT NULL,
  `department_id` int DEFAULT NULL,
  PRIMARY KEY (`UID`),
  UNIQUE KEY `username` (`username`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `department` (`DID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'zx','123456','zx@ucdconnect.ie','DEPARTMENT_MANAGER',1),(2,'lzh','123456','lzh@ucdconnect.ie','DEPARTMENT_MANAGER',2),(3,'nmh','123456','nmh@ucdconnect.ie','DEPARTMENT_MANAGER',3),(4,'wzq','123456','wzq@ucdconnect.ie','DEPARTMENT_MANAGER',4),(5,'ysq','123456','ysq@ucdconnect.ie','DEPARTMENT_MANAGER',5),(6,'zx1','123456','zx1@ucdconnect.ie','DEPARTMENT_MANAGER',6),(7,'lzh1','123456','lzh1@ucdconnect.ie','DEPARTMENT_MANAGER',7),(8,'nmh1','123456','nmh1@ucdconnect.ie','DEPARTMENT_MANAGER',8),(9,'wzq1','123456','wzq1@ucdconnect.ie','DEPARTMENT_MANAGER',9),(11,'zxroot','123456','zxroot@ucdconnect.ie','WASTE_MANAGER',NULL),(12,'lzhroot','123456','lzhroot@ucdconnect.ie','WASTE_MANAGER',NULL),(13,'nmhroot','123456','nmhroot@ucdconnect.ie','WASTE_MANAGER',NULL),(14,'wsqroot','123456','wzqroot@ucdconnect.ie','WASTE_MANAGER',NULL),(15,'ysqoot','123456','ysqroot@ucdconnect.ie','WASTE_MANAGER',NULL),(16,'user1','123456','1@1.com','INDIVIDUAL_USER',NULL),(17,'government1','123456','1@1.com','GOVERNMENT_MANAGER',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usertemplate`
--

DROP TABLE IF EXISTS `usertemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usertemplate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `UID` int NOT NULL,
  `wasteName` varchar(256) NOT NULL,
  `wasteType` enum('HEAVY_METAL_WASTEWATER','EXHAUST_GAS','MINERAL_RESIDUE','CUTTING_FLUID','METAL_CHIPS','PLASTIC','COMPOSITE_MATERIAL_CUTTING_WASTE','WASTE_PAINT','DUST','CHEMICALS','CATALYZER','CHEMICAL_PROPELLANTS','FUEL_RESIDUES','DISCARDED_ELECTRONIC_COMPONENTS','HYDRAULIC_OIL','LUBRICANT_WASTE','HAZARDOUS_CHEMICALS','WASTE_EXPERIMENTAL_EQUIPMENT','WASTE_HEAT','WASTE_PAPER','HOUSEHOLD_WASTE') NOT NULL,
  `attribution` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid_name_unique` (`UID`,`wasteName`),
  CONSTRAINT `usertemplate_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `user` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usertemplate`
--

LOCK TABLES `usertemplate` WRITE;
/*!40000 ALTER TABLE `usertemplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `usertemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `waste`
--

DROP TABLE IF EXISTS `waste`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `waste` (
  `WID` int NOT NULL AUTO_INCREMENT,
  `wasteType` enum('HEAVY_METAL_WASTEWATER','EXHAUST_GAS','MINERAL_RESIDUE','CUTTING_FLUID','METAL_CHIPS','PLASTIC','COMPOSITE_MATERIAL_CUTTING_WASTE','WASTE_PAINT','DUST','CHEMICALS','CATALYZER','CHEMICAL_PROPELLANTS','FUEL_RESIDUES','DISCARDED_ELECTRONIC_COMPONENTS','HYDRAULIC_OIL','LUBRICANT_WASTE','HAZARDOUS_CHEMICALS','WASTE_EXPERIMENTAL_EQUIPMENT','WASTE_HEAT','WASTE_PAPER','HOUSEHOLD_WASTE') NOT NULL,
  `wasteDepartment` enum('METALLURGY','EQUIPMENT_MANUFACTURING','COMPOSITE_MATERIAL','NEW_ENERGY','AUTOMATION_SYSTEM','MAINTENANCE','LABORATORY','DATA_CENTER','OFFICE') DEFAULT NULL,
  `wasteSource` enum('INTERNAL','EXTERNAL','EXTERNALFREE') NOT NULL,
  PRIMARY KEY (`WID`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `waste`
--

LOCK TABLES `waste` WRITE;
/*!40000 ALTER TABLE `waste` DISABLE KEYS */;
INSERT INTO `waste` VALUES (1,'HEAVY_METAL_WASTEWATER','METALLURGY','INTERNAL'),(2,'EXHAUST_GAS','METALLURGY','INTERNAL'),(3,'MINERAL_RESIDUE','METALLURGY','INTERNAL'),(4,'CUTTING_FLUID','EQUIPMENT_MANUFACTURING','INTERNAL'),(5,'METAL_CHIPS','EQUIPMENT_MANUFACTURING','INTERNAL'),(6,'PLASTIC','EQUIPMENT_MANUFACTURING','INTERNAL'),(7,'COMPOSITE_MATERIAL_CUTTING_WASTE','EQUIPMENT_MANUFACTURING','INTERNAL'),(8,'WASTE_PAINT','EQUIPMENT_MANUFACTURING','INTERNAL'),(9,'DUST','COMPOSITE_MATERIAL','INTERNAL'),(10,'CHEMICALS','COMPOSITE_MATERIAL','INTERNAL'),(11,'CATALYZER','COMPOSITE_MATERIAL','INTERNAL'),(12,'CHEMICAL_PROPELLANTS','NEW_ENERGY','INTERNAL'),(13,'FUEL_RESIDUES','NEW_ENERGY','INTERNAL'),(14,'DISCARDED_ELECTRONIC_COMPONENTS','AUTOMATION_SYSTEM','INTERNAL'),(15,'HYDRAULIC_OIL','MAINTENANCE','INTERNAL'),(16,'LUBRICANT_WASTE','MAINTENANCE','INTERNAL'),(17,'HAZARDOUS_CHEMICALS','LABORATORY','INTERNAL'),(18,'WASTE_EXPERIMENTAL_EQUIPMENT','LABORATORY','INTERNAL'),(19,'WASTE_HEAT','DATA_CENTER','INTERNAL'),(20,'WASTE_PAPER','OFFICE','INTERNAL'),(21,'HOUSEHOLD_WASTE','OFFICE','INTERNAL');
/*!40000 ALTER TABLE `waste` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wastestorage`
--

DROP TABLE IF EXISTS `wastestorage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wastestorage` (
  `WSID` int NOT NULL AUTO_INCREMENT,
  `wasteType` enum('HEAVY_METAL_WASTEWATER','EXHAUST_GAS','MINERAL_RESIDUE','CUTTING_FLUID','METAL_CHIPS','PLASTIC','COMPOSITE_MATERIAL_CUTTING_WASTE','WASTE_PAINT','DUST','CHEMICALS','CATALYZER','CHEMICAL_PROPELLANTS','FUEL_RESIDUES','DISCARDED_ELECTRONIC_COMPONENTS','HYDRAULIC_OIL','LUBRICANT_WASTE','HAZARDOUS_CHEMICALS','WASTE_EXPERIMENTAL_EQUIPMENT','WASTE_HEAT','WASTE_PAPER','HOUSEHOLD_WASTE') NOT NULL,
  `maxCapacity` float NOT NULL,
  `currentCapacity` float NOT NULL,
  PRIMARY KEY (`WSID`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wastestorage`
--

LOCK TABLES `wastestorage` WRITE;
/*!40000 ALTER TABLE `wastestorage` DISABLE KEYS */;
INSERT INTO `wastestorage` VALUES (1,'HEAVY_METAL_WASTEWATER',1000,0),(2,'EXHAUST_GAS',2000,47),(3,'MINERAL_RESIDUE',3000,0),(4,'CUTTING_FLUID',4000,31),(5,'METAL_CHIPS',5000,0),(6,'PLASTIC',1100,155),(7,'COMPOSITE_MATERIAL_CUTTING_WASTE',1200,30),(8,'WASTE_PAINT',1300,25),(9,'DUST',1400,0),(10,'CHEMICALS',1500,40),(11,'CATALYZER',1600,0),(12,'CHEMICAL_PROPELLANTS',1700,0),(13,'FUEL_RESIDUES',1800,0),(14,'DISCARDED_ELECTRONIC_COMPONENTS',1900,0),(15,'HYDRAULIC_OIL',2000,0),(16,'LUBRICANT_WASTE',2100,0),(17,'HAZARDOUS_CHEMICALS',2200,0),(18,'WASTE_EXPERIMENTAL_EQUIPMENT',2300,0),(19,'WASTE_HEAT',2400,0),(20,'WASTE_PAPER',2500,0),(21,'HOUSEHOLD_WASTE',2600,0);
/*!40000 ALTER TABLE `wastestorage` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-07 19:55:10
