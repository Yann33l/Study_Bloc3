CREATE DATABASE  IF NOT EXISTS `YannLeg$goldenline` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `YannLeg$goldenline`;
-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: goldenline
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Email` varchar(45) NOT NULL,
  `First_connexion` datetime DEFAULT NULL,
  `Last_change_password` date DEFAULT NULL,
  `Admin` tinyint NOT NULL,
  `Password` varbinary(100) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (15,'aze@aze',NULL,NULL,1,_binary '$2b$12$N4h3dSjGv8nw/OMnkOn4D.LRqopioXMxlKvHAUYvZyqF/eOFdI7/e'),(17,'a@a',NULL,NULL,1,_binary '$2b$12$VOLPMBpuWPEg3Pbi3.wtp.YQAGavtW.HHy8nk/5urexF8X.p.WTrW'),(18,'b@b',NULL,NULL,0,_binary '$2b$12$FVlpch3dxyj7ugXnm0xYOesoxvIu4LZ2yPwWi2nqvDJ1HxdkaFuh2'),(19,'t@t',NULL,NULL,0,_binary '$2b$12$T4Z1yeyZ.34mCmCYfqxRJeSoMWiK6KNnN1lnOxowu6.bv0.AkuPyi'),(20,'c@c',NULL,NULL,0,_binary '$2b$12$9xvrSuKVMHJMMPWPQCLMF.2.FCLwYWVGhvDkw8yXuhvUx9cU4SF56'),(21,'f@f',NULL,NULL,1,_binary '$2b$12$oiN6sRsZU9aWWzU6GwP41uyYTN5HbCUzlfU7DHID9ZfQpLH8nG7yC'),(22,'s@s',NULL,NULL,1,_binary '$2b$12$kRX2qs5x.Xb.eY7UtPmjtuOWrABWQFl/IzvUs0ZBhpO3.ycV8jz/u');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-06  8:19:28
