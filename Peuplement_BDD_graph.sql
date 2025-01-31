-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : db
-- Généré le : mar. 17 déc. 2024 à 13:10
-- Version du serveur : 9.1.0
-- Version de PHP : 8.2.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `AregTec_Drupal`
--

-- --------------------------------------------------------

--
-- Structure de la table `entites`
--

CREATE TABLE `entites` (
  `entite` varchar(50) DEFAULT NULL,
  `x` float DEFAULT NULL,
  `y` float DEFAULT NULL,
  `relie_a` varchar(50) DEFAULT NULL,
  `nom_image` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `entites`
--

INSERT INTO `entites` (`entite`, `x`, `y`, `relie_a`, `nom_image`) VALUES
('Crane', 373, 300, 'C1', 'crane'),
('machoire', 403.5, 443.5, 'Crane', 'Machoire'),
('C1', 654.167, 276.833, 'C2', 'C1'),
('C2', 730.167, 339.5, 'C3', 'C2'),
('C3', 780.833, 415.5, 'C4', 'C3'),
('C4', 840.833, 523.5, 'C5', 'C4'),
('C5', 879.5, 564.833, 'C6', 'C5'),
('C6', 904.833, 615.5, 'C7', 'C6'),
('C7', 959.5, 663.5, 'T1', 'C7'),
('T1', 1008.83, 690.167, 'T2', 'T1'),
('T2', 1026.17, 726.167, 'T3', 'T2'),
('T3', 1080.83, 726.167, 'T4', 'T3'),
('T4', 1134.17, 728.833, 'T5', 'T4'),
('T5', 1186.17, 735.5, 'T6', 'T5'),
('T6', 1240.83, 732.833, 'T7', 'T6'),
('T7', 1310.17, 738.167, 'T8', 'T7'),
('T8', 1384.83, 715.5, 'T9', 'T8'),
('T9', 1433.5, 718.5, 'T10', 'T9'),
('T10', 1478.83, 711.833, 'T11', 'T10'),
('T11', 1518.83, 714.5, 'T12', 'T11'),
('T12', 1562.83, 702.5, 'T13', 'T12'),
('T13', 1617.5, 713.167, 'L1', 'T13'),
('L1', 1656.17, 695.833, 'L2', 'L1'),
('L2', 1742.83, 699.833, 'L3', 'L2'),
('L3', 1809.5, 697.167, 'L4', 'L3'),
('L4', 1868.17, 657.167, 'L5', 'L4'),
('L5', 1945.5, 667.833, 'L6', 'L5'),
('L6', 1998.83, 695.833, 'L7', 'L6'),
('L7', 2070.83, 705.167, 'sacrum', 'L7'),
('sacrum', 2188.17, 731.833, 'caudale 2', 'sacrum'),
('caudale 2', 2286.5, 745.833, 'caudale 3', 'caudale 2'),
('caudale 3', 2315.83, 760.5, 'caudale 4', 'caudale 3'),
('caudale 4', 2343.83, 780.5, 'caudale 5', 'caudale 4'),
('caudale 5', 2365.17, 805.833, 'caudale x', 'caudale 5'),
('caudale x', 2426.5, 863.167, '', 'caudale x'),
('pubis', 1985.17, 757.833, 'L4', 'pubis'),
('femur', 2027.83, 1064.5, 'pubis', 'femur'),
('fibula', 2186.5, 1565.5, 'tibia', 'fibula'),
('tibia', 2146.5, 1583.5, 'femur', 'tibia'),
('calcaneus', 2306.5, 1895.5, 'fibula', 'calcaneus'),
('calcaneus', 2306.5, 1895.5, 'tibia', 'calcaneus'),
('pied arrière gauche', 2297.5, 2150.5, 'calcaneus', 'patte arriere gauche'),
('pied avant gauche', 938.5, 2150.5, 'ulna', 'patte avant gauche'),
('pied avant gauche', 938.5, 2150.5, 'radius', 'patte avant gauche'),
('ulna', 947.5, 1709.5, 'humerus', 'ulna'),
('radius', 915.5, 1765, 'humerus', 'radius'),
('humerus', 801.5, 1225.5, 'scapula', 'humerus'),
('scapula', 842.5, 851.5, 'C7', 'scapula');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
