CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS cafe (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    logo TEXT, 
    location VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS employee (
    id VARCHAR(9) PRIMARY KEY, 
    name VARCHAR(255) NOT NULL,
    email_address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(8) NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female'))
);

CREATE TABLE IF NOT EXISTS employee_cafe (
    employee_id VARCHAR(9) NOT NULL,
    cafe_id UUID NOT NULL,
    start_date DATE NOT NULL,
    PRIMARY KEY (employee_id, cafe_id),
    UNIQUE (employee_id),
    FOREIGN KEY (employee_id) REFERENCES employee (id) ON DELETE CASCADE,
    FOREIGN KEY (cafe_id) REFERENCES cafe (id) ON DELETE CASCADE
);




INSERT INTO employee (id, name, email_address, phone_number, gender) VALUES
('UI0000001', 'Alice', 'alice@email.com', '91111111', 'Female'),
('UI0000002', 'Bob', 'bob@email.com', '82222222', 'Male'),
('UI0000003', 'Charlie', 'charlie@email.com', '93333333', 'Male'),
('UI0000004', 'Diana', 'diana@email.com', '84444444', 'Female'),
('UI0000005', 'Eva', 'eva@email.com', '94689971', 'Female'),
('UI0000006', 'Francis', 'francis@email.com', '80360074', 'Male');

INSERT INTO cafe (id, name, description, logo, location) VALUES
('fd695398-789f-4b00-8e4c-1c198c8f3024', 'Lola''s', 'Discover Lola''s Cafe, your neighborhood spot in Singapore for fresh coffee, baked treats, and hearty brunches. Join us for great food and cozy ambiance.', '/logos/fd695398-789f-4b00-8e4c-1c198c8f3024/lola.png', 'Tampines'),
('fe888e07-c516-4607-aa47-3a948c681f4d', 'Columbus', 'Casual corner cafe offering brunch staples, waffles & a global menu, plus coffee & pressed juice.', '/logos/fe888e07-c516-4607-aa47-3a948c681f4d/columbus.jpg', 'Upper Thomson'),
('4c7ba93c-3ef3-4766-8d99-e76bfd2975e3', 'KOOKS C', 'Kooks Creamery specializes in creating artisan ice cream and molten lava cookies.', '/logos/4c7ba93c-3ef3-4766-8d99-e76bfd2975e3/kooks.png', 'Serangoon'),
('1c19d74e-2af5-48a1-8ee6-91203b1dc001', 'Arigato', 'Enjoy some Japanese inspired comfort food and specialty coffee paired with honest hospitality, now serving in the charming neighbourhood of Thomson.', '/logos/1c19d74e-2af5-48a1-8ee6-91203b1dc001/arigato.png', 'Upper Thomson');

INSERT INTO employee_cafe (employee_id, cafe_id, start_date) VALUES
('UI0000001', 'fd695398-789f-4b00-8e4c-1c198c8f3024', '2023-01-15'),
('UI0000002', 'fe888e07-c516-4607-aa47-3a948c681f4d', '2023-02-20'),
('UI0000003', '4c7ba93c-3ef3-4766-8d99-e76bfd2975e3', '2023-03-10'),
('UI0000004', 'fd695398-789f-4b00-8e4c-1c198c8f3024', '2023-04-05'),
('UI0000005', '1c19d74e-2af5-48a1-8ee6-91203b1dc001', '2024-07-11'),
('UI0000006', '1c19d74e-2af5-48a1-8ee6-91203b1dc001', '2025-05-15');

