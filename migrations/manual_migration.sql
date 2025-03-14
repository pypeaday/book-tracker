-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP
);

-- Create indexes for users table
CREATE INDEX IF NOT EXISTS ix_users_id ON users (id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);

-- Add user_id column to books table if it doesn't exist
PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

-- Check if user_id column exists in books table
SELECT CASE 
    WHEN COUNT(*) = 0 THEN (
        -- Add user_id column to books table
        ALTER TABLE books ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    )
    ELSE (
        SELECT 'Column user_id already exists in books table'
    )
END
FROM pragma_table_info('books') 
WHERE name = 'user_id';

COMMIT;

PRAGMA foreign_keys=on;
