-- ================================================================================
-- ROYAL ENFIELD ERP ANALYTICS - PRODUCTION DDL SCHEMA
-- Compatible with PostgreSQL, MySQL, SQLite, and SQL Server
-- ================================================================================

-- --------------------------------------------------------------------------------
-- Table 1: Motorcycles (Master Catalog)
-- --------------------------------------------------------------------------------
CREATE TABLE Motorcycles (
    Bike_ID VARCHAR(10) PRIMARY KEY,
    Model VARCHAR(50) NOT NULL,
    Engine_CC INT NOT NULL,
    Category VARCHAR(30) NOT NULL,
    Fuel_Type VARCHAR(15) NOT NULL DEFAULT 'Petrol',
    Transmission VARCHAR(15) NOT NULL,
    Mileage_kmpl DECIMAL(4,1) NOT NULL,
    Fuel_Tank_L DECIMAL(4,1) NOT NULL,
    Ex_Showroom_Price INT NOT NULL,
    Launch_Year INT NOT NULL
);

-- --------------------------------------------------------------------------------
-- Table 2: Dealers (Showroom & Channel Directory)
-- --------------------------------------------------------------------------------
CREATE TABLE Dealers (
    Dealer_ID VARCHAR(10) PRIMARY KEY,
    Dealer_Name VARCHAR(100) NOT NULL,
    Dealer_Type VARCHAR(30) NOT NULL,
    State VARCHAR(50) NOT NULL,
    City VARCHAR(50) NOT NULL,
    Region VARCHAR(15) NOT NULL,
    Opening_Year INT NOT NULL,
    Sales_Target INT NOT NULL,
    Dealer_Rating DECIMAL(2,1) NOT NULL
);

-- --------------------------------------------------------------------------------
-- Table 3: Employees (Staff & Workforce)
-- --------------------------------------------------------------------------------
CREATE TABLE Employees (
    Employee_ID VARCHAR(10) PRIMARY KEY,
    Employee_Name VARCHAR(80) NOT NULL,
    Dealer_ID VARCHAR(10) NOT NULL,
    Department VARCHAR(30) NOT NULL,
    Designation VARCHAR(50) NOT NULL,
    Experience_Years INT NOT NULL,
    Monthly_Target INT NOT NULL,
    Salary INT NOT NULL,
    Joining_Date DATE NOT NULL,
    FOREIGN KEY (Dealer_ID) REFERENCES Dealers(Dealer_ID)
);

-- --------------------------------------------------------------------------------
-- Table 4: Customers (Demographics & Profiles)
-- --------------------------------------------------------------------------------
CREATE TABLE Customers (
    Customer_ID VARCHAR(10) PRIMARY KEY,
    Customer_Name VARCHAR(80) NOT NULL,
    Age INT NOT NULL,
    Age_Group VARCHAR(15) NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Occupation VARCHAR(40) NOT NULL,
    Annual_Income INT NOT NULL,
    Marital_Status VARCHAR(15) NOT NULL,
    State VARCHAR(50) NOT NULL,
    City VARCHAR(50) NOT NULL,
    Customer_Segment VARCHAR(30) NOT NULL,
    Registration_Date DATE NOT NULL
);

-- --------------------------------------------------------------------------------
-- Table 5: Sales (Commercial Vehicle Transactions)
-- --------------------------------------------------------------------------------
CREATE TABLE Sales (
    Sale_ID VARCHAR(10) PRIMARY KEY,
    Sale_Date DATE NOT NULL,
    Customer_ID VARCHAR(10) NOT NULL,
    Dealer_ID VARCHAR(10) NOT NULL,
    Employee_ID VARCHAR(10) NOT NULL,
    Bike_ID VARCHAR(10) NOT NULL,
    Payment_Mode VARCHAR(20) NOT NULL,
    Ex_Showroom_Price INT NOT NULL,
    Discount_Amount INT NOT NULL DEFAULT 0,
    On_Road_Price INT NOT NULL,
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Dealer_ID) REFERENCES Dealers(Dealer_ID),
    FOREIGN KEY (Employee_ID) REFERENCES Employees(Employee_ID),
    FOREIGN KEY (Bike_ID) REFERENCES Motorcycles(Bike_ID)
);

-- --------------------------------------------------------------------------------
-- Table 6: Finance (Loan Contracts & Financing)
-- --------------------------------------------------------------------------------
CREATE TABLE Finance (
    Finance_ID VARCHAR(10) PRIMARY KEY,
    Sale_ID VARCHAR(10) NOT NULL UNIQUE,
    Customer_ID VARCHAR(10) NOT NULL,
    Bank VARCHAR(50) NOT NULL,
    Loan_Amount INT NOT NULL,
    Down_Payment INT NOT NULL,
    Tenure_Months INT NOT NULL,
    Interest_Rate_Pct DECIMAL(4,2) NOT NULL,
    EMI INT NOT NULL,
    FOREIGN KEY (Sale_ID) REFERENCES Sales(Sale_ID),
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID)
);

-- --------------------------------------------------------------------------------
-- Table 7: Service (After-Sales Maintenance & Repairs)
-- --------------------------------------------------------------------------------
CREATE TABLE Service (
    Service_ID VARCHAR(10) PRIMARY KEY,
    Service_Date DATE NOT NULL,
    Sale_ID VARCHAR(10) NOT NULL,
    Customer_ID VARCHAR(10) NOT NULL,
    Dealer_ID VARCHAR(10) NOT NULL,
    Bike_ID VARCHAR(10) NOT NULL,
    Service_Type VARCHAR(30) NOT NULL,
    Odometer_Reading_km INT NOT NULL,
    Parts_Cost INT NOT NULL DEFAULT 0,
    Labor_Cost INT NOT NULL DEFAULT 0,
    Total_Service_Cost INT NOT NULL,
    Service_Rating INT NOT NULL,
    FOREIGN KEY (Sale_ID) REFERENCES Sales(Sale_ID),
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Dealer_ID) REFERENCES Dealers(Dealer_ID),
    FOREIGN KEY (Bike_ID) REFERENCES Motorcycles(Bike_ID)
);

-- --------------------------------------------------------------------------------
-- Table 8: WarrantyClaims (Warranty Component Claims)
-- --------------------------------------------------------------------------------
CREATE TABLE WarrantyClaims (
    Claim_ID VARCHAR(10) PRIMARY KEY,
    Claim_Date DATE NOT NULL,
    Service_ID VARCHAR(10) NOT NULL,
    Sale_ID VARCHAR(10) NOT NULL,
    Customer_ID VARCHAR(10) NOT NULL,
    Dealer_ID VARCHAR(10) NOT NULL,
    Bike_ID VARCHAR(10) NOT NULL,
    Component_Category VARCHAR(40) NOT NULL,
    Claim_Amount INT NOT NULL,
    Claim_Status VARCHAR(25) NOT NULL,
    Approved_Amount INT NOT NULL DEFAULT 0,
    FOREIGN KEY (Service_ID) REFERENCES Service(Service_ID),
    FOREIGN KEY (Sale_ID) REFERENCES Sales(Sale_ID),
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Dealer_ID) REFERENCES Dealers(Dealer_ID),
    FOREIGN KEY (Bike_ID) REFERENCES Motorcycles(Bike_ID)
);

-- --------------------------------------------------------------------------------
-- Table 9: Accessories (Genuine Accessories Transactions)
-- --------------------------------------------------------------------------------
CREATE TABLE Accessories (
    Accessory_Sale_ID VARCHAR(10) PRIMARY KEY,
    Purchase_Date DATE NOT NULL,
    Customer_ID VARCHAR(10) NOT NULL,
    Dealer_ID VARCHAR(10) NOT NULL,
    Bike_ID VARCHAR(10) NOT NULL,
    Accessory_Name VARCHAR(80) NOT NULL,
    Category VARCHAR(40) NOT NULL,
    Quantity INT NOT NULL DEFAULT 1,
    Unit_Price INT NOT NULL,
    Total_Amount INT NOT NULL,
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Dealer_ID) REFERENCES Dealers(Dealer_ID),
    FOREIGN KEY (Bike_ID) REFERENCES Motorcycles(Bike_ID)
);

-- --------------------------------------------------------------------------------
-- Table 10: Inventory (Stock Level Snapshots)
-- --------------------------------------------------------------------------------
CREATE TABLE Inventory (
    Inventory_ID VARCHAR(10) PRIMARY KEY,
    Dealer_ID VARCHAR(10) NOT NULL,
    Bike_ID VARCHAR(10) NOT NULL,
    Item_Type VARCHAR(25) NOT NULL,
    Item_Name VARCHAR(80) NOT NULL,
    Opening_Stock INT NOT NULL DEFAULT 0,
    Received_Stock INT NOT NULL DEFAULT 0,
    Sold_Stock INT NOT NULL DEFAULT 0,
    Closing_Stock INT NOT NULL DEFAULT 0,
    Reorder_Level INT NOT NULL DEFAULT 10,
    Stock_Value_INR INT NOT NULL DEFAULT 0,
    Last_Restock_Date DATE NOT NULL,
    FOREIGN KEY (Dealer_ID) REFERENCES Dealers(Dealer_ID),
    FOREIGN KEY (Bike_ID) REFERENCES Motorcycles(Bike_ID)
);

-- --------------------------------------------------------------------------------
-- Table 11: TestRide (CRM Leads & Test Ride Logs)
-- --------------------------------------------------------------------------------
CREATE TABLE TestRide (
    Test_Ride_ID VARCHAR(10) PRIMARY KEY,
    Test_Ride_Date DATE NOT NULL,
    Customer_ID VARCHAR(10) NOT NULL,
    Dealer_ID VARCHAR(10) NOT NULL,
    Bike_ID VARCHAR(10) NOT NULL,
    Test_Ride_Status VARCHAR(20) NOT NULL,
    Duration_Minutes INT NOT NULL DEFAULT 0,
    Feedback_Rating INT NOT NULL DEFAULT 0,
    Converted_To_Sale VARCHAR(5) NOT NULL DEFAULT 'No',
    Sale_ID VARCHAR(10),
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Dealer_ID) REFERENCES Dealers(Dealer_ID),
    FOREIGN KEY (Bike_ID) REFERENCES Motorcycles(Bike_ID)
);

-- --------------------------------------------------------------------------------
-- INDEXES FOR QUERY OPTIMIZATION
-- --------------------------------------------------------------------------------
CREATE INDEX idx_sales_dealer ON Sales(Dealer_ID);
CREATE INDEX idx_sales_customer ON Sales(Customer_ID);
CREATE INDEX idx_sales_bike ON Sales(Bike_ID);
CREATE INDEX idx_sales_date ON Sales(Sale_Date);

CREATE INDEX idx_service_sale ON Service(Sale_ID);
CREATE INDEX idx_service_dealer ON Service(Dealer_ID);
CREATE INDEX idx_service_date ON Service(Service_Date);

CREATE INDEX idx_finance_sale ON Finance(Sale_ID);
CREATE INDEX idx_warranty_service ON WarrantyClaims(Service_ID);
CREATE INDEX idx_testride_customer ON TestRide(Customer_ID);
CREATE INDEX idx_testride_sale ON TestRide(Sale_ID);
