
-- Add columns for storing RAG multimedia links
ALTER TABLE sakhi_conversations ADD COLUMN IF NOT EXISTS youtube_link text;
ALTER TABLE sakhi_conversations ADD COLUMN IF NOT EXISTS infographic_url text;
