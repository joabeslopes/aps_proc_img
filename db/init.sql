USE aps_database;

CREATE TABLE aps_moradores (
    id INT AUTO_INCREMENT,
    nome VARCHAR(30) NOT NULL,

    primary key(id)
);

CREATE TABLE aps_veiculos (
id INT AUTO_INCREMENT,
placa CHAR(7) NOT NULL UNIQUE,
marca VARCHAR(30),
id_morador INT NOT NULL,

primary key(id),
constraint fk_morador foreign key(id_morador) references aps_moradores(id)
);

INSERT INTO aps_moradores(id, nome) VALUES
(1, 'João'),
(2, 'Marcos'),
(3, 'Rafael');

INSERT INTO aps_veiculos(placa,marca,id_morador) VALUES
('GIK4130','FORD',1),
('GIS3F45','VOLKSWAGEN',2),
('EVG9F80','HYUNDAI',3);
