-- =====================================================
-- Personalization Journey Table
-- Run this in Supabase SQL Editor
-- =====================================================

CREATE TABLE IF NOT EXISTS sakhi_user_journeys (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES sakhi_users(user_id) ON DELETE CASCADE,
    stage TEXT NOT NULL,
    date DATE,
    date_type TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_user_journey UNIQUE(user_id)
);

-- Note: unique_user_journey ensures a user only has one active journey stage at a time.
-- Updating their stage will overwrite the previous one.
