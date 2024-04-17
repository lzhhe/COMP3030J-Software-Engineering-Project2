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
INSERT INTO `alembic_version` VALUES ('23180e8ad8d3');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,1,'2023-04-10','Metal Wastewater Disposal','HEAVY_METAL_WASTEWATER',500,'CuSo4:10%',1,'Metal Wastewater Disposal','UNCONFIRMED',1),(2,2,'2023-04-12','Exhaust Gas Treatment','EXHAUST_GAS',20,'So2:10%',1,'Exhaust Gas Treatment','UNCONFIRMED',2),(3,3,'2023-04-15','Cutting Fluid Recycling','CUTTING_FLUID',15,'waste oil:100%',1,'Cutting Fluid Recycling','UNCONFIRMED',3),(4,4,'2023-04-18','Plastic Waste Management','PLASTIC',80,'PVC:100%',1,'Plastic Waste Management','UNCONFIRMED',4),(5,5,'2023-04-20','Chemical Propellant Disposal','CHEMICALS',40,'C2H2:20%',1,'Chemical Propellant Disposal','UNCONFIRMED',5);
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
INSERT INTO `processcapacity` VALUES (1,'HEAVY_METAL_WASTEWATER',10000,0),(2,'EXHAUST_GAS',1000,0),(3,'MINERAL_RESIDUE',1000,0),(4,'CUTTING_FLUID',1000,0),(5,'METAL_CHIPS',1000,0),(6,'PLASTIC',1000,0),(7,'COMPOSITE_MATERIAL_CUTTING_WASTE',1000,0),(8,'WASTE_PAINT',1000,0),(9,'DUST',1000,0),(10,'CHEMICALS',1000,0),(11,'CATALYZER',1000,0),(12,'CHEMICAL_PROPELLANTS',1000,0),(13,'FUEL_RESIDUES',1000,0),(14,'DISCARDED_ELECTRONIC_COMPONENTS',1000,0),(15,'HYDRAULIC_OIL',1000,0),(16,'LUBRICANT_WASTE',1000,0),(17,'HAZARDOUS_CHEMICALS',1000,0),(18,'WASTE_EXPERIMENTAL_EQUIPMENT',1000,0),(19,'WASTE_HEAT',1000,0),(20,'WASTE_PAPER',1000,0),(21,'HOUSEHOLD_WASTE',1000,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'zx','123456','zx@ucdconnect.ie','DEPARTMENT_MANAGER',1),(2,'lzh','123456','lzh@ucdconnect.ie','DEPARTMENT_MANAGER',2),(3,'nmh','123456','nmh@ucdconnect.ie','DEPARTMENT_MANAGER',3),(4,'wzq','123456','wzq@ucdconnect.ie','DEPARTMENT_MANAGER',4),(5,'ysq','123456','ysq@ucdconnect.ie','DEPARTMENT_MANAGER',5),(11,'zxroot','123456','zxroot@ucdconnect.ie','WASTE_MANAGER',NULL),(12,'lzhroot','123456','lzhroot@ucdconnect.ie','WASTE_MANAGER',NULL),(13,'nmhroot','123456','nmhroot@ucdconnect.ie','WASTE_MANAGER',NULL),(14,'wsqroot','123456','wzqroot@ucdconnect.ie','WASTE_MANAGER',NULL),(15,'ysqoot','123456','ysqroot@ucdconnect.ie','WASTE_MANAGER',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
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
INSERT INTO `wastestorage` VALUES (1,'HEAVY_METAL_WASTEWATER',1000,0),(2,'EXHAUST_GAS',2000,0),(3,'MINERAL_RESIDUE',3000,0),(4,'CUTTING_FLUID',4000,0),(5,'METAL_CHIPS',5000,0),(6,'PLASTIC',1100,0),(7,'COMPOSITE_MATERIAL_CUTTING_WASTE',1200,0),(8,'WASTE_PAINT',1300,0),(9,'DUST',1400,0),(10,'CHEMICALS',1500,0),(11,'CATALYZER',1600,0),(12,'CHEMICAL_PROPELLANTS',1700,0),(13,'FUEL_RESIDUES',1800,0),(14,'DISCARDED_ELECTRONIC_COMPONENTS',1900,0),(15,'HYDRAULIC_OIL',2000,0),(16,'LUBRICANT_WASTE',2100,0),(17,'HAZARDOUS_CHEMICALS',2200,0),(18,'WASTE_EXPERIMENTAL_EQUIPMENT',2300,0),(19,'WASTE_HEAT',2400,0),(20,'WASTE_PAPER',2500,0),(21,'HOUSEHOLD_WASTE',2600,0);
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

-- Dump completed on 2024-04-17 20:22:26
