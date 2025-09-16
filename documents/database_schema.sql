CREATE TYPE user_role AS ENUM ('admin', 'area_manager', 'auditor');
CREATE TYPE user_status AS ENUM ('active', 'inactive');
CREATE TYPE visit_status AS ENUM ('in_progress', 'completed');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    name VARCHAR,
    role user_role NOT NULL,
    status user_status NOT NULL
);

CREATE TABLE audit_visits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    store_id UUID NOT NULL,
    auditor_id UUID NOT NULL,
    template_id UUID NOT NULL,
    visit_datetime TIMESTAMPTZ NOT NULL,
    status visit_status NOT NULL
);