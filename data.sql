-- MySQL dump 10.16  Distrib 10.1.48-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	10.1.48-MariaDB-0+deb9u2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dbo.user_preference`
--

DROP TABLE IF EXISTS `dbo.user_preference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbo.user_preference` (
  `id` tinyint(4) DEFAULT NULL,
  `user_id` tinyint(4) DEFAULT NULL,
  `category_name` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dbo.user_preference`
--

LOCK TABLES `dbo.user_preference` WRITE;
/*!40000 ALTER TABLE `dbo.user_preference` DISABLE KEYS */;
INSERT INTO `dbo.user_preference` VALUES (1,1,'Music'),(2,1,'Technology'),(3,2,'Technology'),(4,2,'Sports'),(5,2,'Art'),(6,2,'Business'),(7,2,'Education'),(8,2,'Music'),(9,3,'Sports'),(10,3,'Education'),(11,3,'Technology'),(12,3,'Music'),(13,3,'Art'),(14,3,'Business'),(21,4,'Sports'),(22,5,'Technology'),(23,5,'Music'),(24,5,'Art'),(25,5,'Business');
/*!40000 ALTER TABLE `dbo.user_preference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dbo.users`
--

DROP TABLE IF EXISTS `dbo.users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbo.users` (
  `id` tinyint(4) DEFAULT NULL,
  `name` varchar(3) DEFAULT NULL,
  `email` varchar(19) DEFAULT NULL,
  `password` smallint(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dbo.users`
--

LOCK TABLES `dbo.users` WRITE;
/*!40000 ALTER TABLE `dbo.users` DISABLE KEYS */;
INSERT INTO `dbo.users` VALUES (1,'ze','zeyad@gmail.com',233),(2,'amr','amr.emara@gmail.com',345),(3,'w','z@gmail.com',111),(4,'w','w@gmail.com',123),(5,'eee','mk@gmail.com',123);
/*!40000 ALTER TABLE `dbo.users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-30 16:42:40
