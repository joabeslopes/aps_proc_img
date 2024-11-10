USE aps_database;

CREATE TABLE aps_veiculos (
id INT AUTO_INCREMENT,
placa CHAR(7) NOT NULL,
marca VARCHAR(30),
modelo VARCHAR(30),

primary key(id)
);


INSERT INTO aps_veiculos(placa,marca,modelo) VALUES
('CSA5J19','VOLKSWAGEN','PARATI'),
('FJY2E56','VOLKSWAGEN','POLO TRACK'),
('FOL7B05','CHEVROLET','COBALT');
