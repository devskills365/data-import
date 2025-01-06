CREATE DATABASE anstat_base_regionale;
USE anstat_base_regionale;

-- Table: Domaines
CREATE TABLE Domaines (
    idDomaines VARCHAR(10) PRIMARY KEY NOT NULL,
    nomDomaines VARCHAR(255) NOT NULL
);
-- Table: Sous_Domaines
CREATE TABLE Sous_Domaines (
    idSousDomaines VARCHAR(10) PRIMARY KEY,
    f_idDomaines VARCHAR(10) NOT NULL,
    nomSousDomaines VARCHAR(255) NOT NULL,
    FOREIGN KEY (f_idDomaines) REFERENCES Domaines(idDomaines)
);

-- Table: Indicateurs    
CREATE TABLE Indicateurs (
    idIndicateurs VARCHAR(10) PRIMARY KEY,
    f_idSousDomaines VARCHAR(10) ,
    nomIndicateur VARCHAR(255) NOT NULL,
    definition TEXT,
     FOREIGN KEY (f_idSousDomaines) REFERENCES Sous_Domaines(idSousDomaines)
);


-- Table: Annees

CREATE TABLE Annees (
    idAnnees VARCHAR(10) PRIMARY KEY,
    valAnnees INT NOT NULL
);



-- Table: Dimensions
CREATE TABLE Dimensions (
    idDimensions VARCHAR(10) PRIMARY KEY,
    nomDimension VARCHAR(255) NOT NULL
);

-- Table: Modalites
CREATE TABLE Modalites (
    idModalites VARCHAR(10) PRIMARY KEY,
    f_idDimensions VARCHAR(10),
    nomModalites VARCHAR(255) NOT NULL,
    FOREIGN KEY (f_idDimensions) REFERENCES Dimensions(idDimensions)
);
-- Table: Donnees
CREATE TABLE Donnees (
    idDonnees INT AUTO_INCREMENT PRIMARY KEY,
    f_idIndicateurs VARCHAR(10) NOT NULL,
    f_idAnnees VARCHAR(10) NOT NULL,
    valDonnees DECIMAL(10, 2),
    FOREIGN KEY (f_idIndicateurs) REFERENCES Indicateurs(idIndicateurs),
    FOREIGN KEY (f_idAnnees) REFERENCES Annees(idAnnees)
);
-- Table: Donnees_modalites
CREATE TABLE Donnees_modalites (
    idDonnees_modalites INT AUTO_INCREMENT PRIMARY KEY,
    f_idDonnees INT,
    f_idModalites  VARCHAR(10),
    FOREIGN KEY (f_idDonnees) REFERENCES Donnees(idDonnees),
    FOREIGN KEY (f_idModalites) REFERENCES Modalites(idModalites),
    UNIQUE KEY unique_donnee_modalite (f_idDonnees, f_idModalites) -- Pour éviter les doublons
);

ALTER TABLE Dimensions MODIFY nomDimension VARCHAR(255) COLLATE utf8mb4_general_ci;
ALTER TABLE Modalites MODIFY nomModalites VARCHAR(255) COLLATE utf8mb4_general_ci;
ALTER TABLE Indicateurs MODIFY nomIndicateur VARCHAR(255) COLLATE utf8mb4_general_ci;




