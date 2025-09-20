-- Central Command Center Database Extensions
-- Extends existing AudEasy schema for multi-vertical management

-- Verticals Management Table
CREATE TABLE verticals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'planning',
    description TEXT,
    tech_stack JSONB,
    revenue_model VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects Table (spans across all verticals)
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    vertical_id INTEGER REFERENCES verticals(id),
    client_id INTEGER REFERENCES users(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'inquiry',
    budget_min DECIMAL(10,2),
    budget_max DECIMAL(10,2),
    start_date DATE,
    end_date DATE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Service Health Monitoring
CREATE TABLE service_health (
    id SERIAL PRIMARY KEY,
    vertical_id INTEGER REFERENCES verticals(id),
    service_url VARCHAR(255),
    status_code INTEGER,
    response_time_ms INTEGER,
    error_message TEXT,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Revenue Tracking
CREATE TABLE revenue_records (
    id SERIAL PRIMARY KEY,
    vertical_id INTEGER REFERENCES verticals(id),
    project_id INTEGER REFERENCES projects(id),
    amount DECIMAL(10,2) NOT NULL,
    type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System Metrics
CREATE TABLE system_metrics (
    id SERIAL PRIMARY KEY,
    metric_type VARCHAR(50) NOT NULL,
    vertical_id INTEGER REFERENCES verticals(id),
    value DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial verticals
INSERT INTO verticals (name, display_name, status, description, tech_stack, revenue_model) VALUES
('audeasy', 'AudEasy', 'live', 'Audit & Compliance Management System', '{"backend": "Flask", "database": "PostgreSQL", "frontend": "HTML/JS"}', 'saas_subscription'),
('webflow', 'WebFlow', 'ready', 'Website Development & Management', '{"cms": "WordPress/Ghost", "tools": "Figma/GitHub", "hosting": "Cloudflare"}', 'project_plus_hosting'),
('design3d', 'Design3D', 'ready', '3D Modeling & Visualization', '{"tools": "SketchUp/AutoCAD", "rendering": "Cloud", "storage": "Cloudinary"}', 'project_based');
