create database marthos;

use marthos;

create table IF NOT EXISTS Ville (
    Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Nom varchar(256)
    ) ENGINE=InnoDB;

create table IF NOT EXISTS Gare (
    Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Nom varchar(256),
    IdVille INT,
    FOREIGN KEY (IdVille) REFERENCES Ville(Id)
    ) ENGINE=InnoDB;

create table Dessert(
    IdVille int NOT NULL,
    IdGare int NOT NULL,
    FOREIGN KEY (IdVille) REFERENCES Ville(Id),
    FOREIGN KEY (IdGare) REFERENCES Gare(Id)
                    ) ENGINE=Innodb;

CREATE table IF NOT EXISTS Companie (
	Id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Nom varchar(100),
	Annule BOOLEAN
	) ENGINE=Innodb;


CREATE table IF NOT EXISTS Train(
	Numero INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	HeureDep varchar(5),
	HeureArrive varchar(5),
	DateDep varchar(100),
	DateArrive varchar(100),
    IdCompanie INT,
    FOREIGN KEY (IdCompanie) REFERENCES Companie(Id)
	) ENGINE=InnoDB;

CREATE table IF NOT EXISTS Arret(
	HeureArrive varchar(5),
	HeureDep varchar(5),
	IdGare INT,
	IdTrain INT,
	FOREIGN KEY (IdGare) REFERENCES Gare(Id),
	FOREIGN KEY (IdTrain) REFERENCES Train(Numero)
	) ENGINE=Innodb;

CREATE table IF NOT EXISTS Passager(
	Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Nom VARCHAR(100),
	Prenom VARCHAR(100)
	) ENGINE=InnoDB;


CREATE table IF NOT EXISTS Client(
	Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Nom varchar(100),
	Prenom varchar(100),
	Adresse varchar (256),
	Telephone varchar(10)
	) ENGINE=InnoDB;

CREATE table IF NOT EXISTS CC (
	IdCompanie INT,
	IdClient INT,
	FOREIGN KEY (IdCompanie) REFERENCES Companie(id),
	FOREIGN KEY (IdClient) REFERENCES Client(id)
	) ENGINE=Innodb;

CREATE table IF NOT EXISTS Reservation (
	Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Confirme BOOLEAN,
	Annule BOOLEAN,
	IdPassager INT,
	IdClient INT,
	IdCompanie INT,
	IdTrain INT,
	FOREIGN KEY (IdPassager) REFERENCES Passager(Id),
	FOREIGN KEY (IdClient) REFERENCES Client(Id),
	FOREIGN KEY (IdCompanie) REFERENCES Companie(Id),
	FOREIGN KEY (IdTrain) REFERENCES Train(Numero)
	) ENGINE=InnoDB;
