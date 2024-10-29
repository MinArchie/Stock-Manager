	DROP DATABASE  StockManagementDB;
	CREATE DATABASE IF NOT EXISTS StockManagementDB;
	USE StockManagementDB;
	CREATE TABLE ASSETS(a_id INT PRIMARY KEY AUTO_INCREMENT,a_name VARCHAR(100) NOT NULL,
		a_type ENUM('Tangible', 'Intangible') NOT NULL,
		category ENUM('Buildings', 'Machinery', 'Cash', 'Inventory', 'Equipment', 'Vehicles', 
					  'Furniture', 'Valuable Antiques', 'Copyrights', 'Brand Recognition', 
					  'Trademarks', 'Patents', 'Intellectual Property', 'Goodwill', 
					  'Franchises', 'Cash Equivalents') NOT NULL,
		a_qty INT DEFAULT 0 ,
		market_price DECIMAL(15,2) NOT NULL,
		a_purchasecost DECIMAL(15,2),
		asset_status ENUM('Active', 'In Repair', 'Decommissioned') DEFAULT 'Active',
		 last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
		a_description TEXT);
	INSERT INTO ASSETS (a_id ,a_name, a_type ,category ,market_price ,a_purchasecost ,asset_status ,last_updated ,a_description )VALUES 
	(1,'Laptop', 'Tangible', 'Equipment',1200.00, 60000.00, 'Active', CURRENT_TIMESTAMP, 'HP Pavilion 15 ');
	
    UPDATE ASSETS 
	SET a_qty = 10 
	WHERE a_id = 1;

	

	CREATE TABLE INVENTORY (
	i_id INT PRIMARY KEY AUTO_INCREMENT,
	i_qty INT DEFAULT 0, 
	a_id INT,
	FOREIGN KEY (a_id) REFERENCES ASSETS(a_id) ON DELETE CASCADE,
	 movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	 status ENUM('In', 'Out') NOT NULL,
	 acquired_price DECIMAL(15,2),                
		market_value DECIMAL(15,2),                  
		profit_loss DECIMAL(15,2) AS (
			CASE
				WHEN status = 'Out' THEN (market_value - acquired_price) * i_qty
				ELSE NULL
			END
		) STORED,     
	 remarks TEXT);
	 
	CREATE INDEX idx_a_type ON ASSETS(a_type);                   
	CREATE INDEX idx_last_updated ON ASSETS(last_updated);        

	CREATE INDEX idx_a_id ON INVENTORY(a_id);                     
	CREATE INDEX idx_status ON INVENTORY(status);                 

	ALTER TABLE ASSETS 
		ADD CONSTRAINT chk_a_qty CHECK (a_qty >= 0),
		ADD CONSTRAINT chk_market_price CHECK (market_price > 0);
	ALTER TABLE ASSETS 
		MODIFY a_name VARCHAR(100) NOT NULL;
	ALTER TABLE INVENTORY 
		ADD CONSTRAINT chk_i_qty CHECK (i_qty >= 0),
		ADD CONSTRAINT chk_acquired_price CHECK (acquired_price >= 0),
		ADD CONSTRAINT chk_market_value CHECK (market_value >= 0);
	SELECT A.a_id, A.a_name, A.a_qty, I.i_qty, I.status
	FROM ASSETS A
	LEFT JOIN INVENTORY I ON A.a_id = I.a_id;


	SELECT A.a_id, A.a_name, A.a_qty, I.i_qty, I.status
	FROM ASSETS A
	RIGHT JOIN INVENTORY I ON A.a_id = I.a_id;




	SELECT A.a_id, A.a_name, SUM(I.i_qty) AS total_qty
	FROM ASSETS A
	LEFT JOIN INVENTORY I ON A.a_id = I.a_id
	GROUP BY A.a_id
	ORDER BY total_qty DESC;

	SELECT A.a_id, A.a_name, A.a_qty, I.i_qty, I.status
	FROM ASSETS A
	LEFT JOIN INVENTORY I ON A.a_id = I.a_id
	UNION
	SELECT A.a_id, A.a_name, A.a_qty, I.i_qty, I.status
	FROM ASSETS A
	RIGHT JOIN INVENTORY I ON A.a_id = I.a_id;

	SELECT A.a_id, A.a_name
	FROM ASSETS A
	WHERE A.a_id IN (
		SELECT I.a_id
		FROM INVENTORY I
		WHERE I.status = 'Out'
	);
