-- =====================================================
-- Auth & Data Persistence Migration
-- Run this in Supabase SQL Editor
-- =====================================================

-- 1. Add Google OAuth fields to existing sakhi_users table
ALTER TABLE sakhi_users 
  ADD COLUMN IF NOT EXISTS google_id TEXT,
  ADD COLUMN IF NOT EXISTS profile_picture TEXT,
  ADD COLUMN IF NOT EXISTS auth_provider TEXT DEFAULT 'email';  -- 'email' or 'google'

-- 2. Tool Usage Table (linked to sakhi_users via user_id)
CREATE TABLE IF NOT EXISTS sakhi_tool_usage (
  id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id     TEXT        NOT NULL REFERENCES sakhi_users(user_id) ON DELETE CASCADE,
  tool_name   TEXT        NOT NULL,         -- e.g. 'ovulation_calculator', 'due_date_calculator'
  tool_data   JSONB       NOT NULL DEFAULT '{}', -- the inputs/outputs of the tool
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast lookups by user
CREATE INDEX IF NOT EXISTS idx_tool_usage_user_id ON sakhi_tool_usage(user_id);

-- 3. User Sessions Table (optional but useful for multi-device logout)
-- Stores JWT tokens so we can invalidate them
CREATE TABLE IF NOT EXISTS sakhi_user_sessions (
  id           UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id      TEXT        NOT NULL REFERENCES sakhi_users(user_id) ON DELETE CASCADE,
  token_hash   TEXT        NOT NULL,   -- hashed JWT for security
  created_at   TIMESTAMPTZ DEFAULT NOW(),
  expires_at   TIMESTAMPTZ,
  is_active    BOOLEAN     DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sakhi_user_sessions(user_id);

-- =====================================================
-- NOTES:
-- - sakhi_tool_usage.user_id references sakhi_users.user_id
-- - sakhi_user_sessions.user_id references sakhi_users.user_id
-- - Deleting a user cascades to both tables
-- =====================================================
