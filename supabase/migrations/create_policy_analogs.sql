/*
  # Create policy_analogs table

  1. New Tables
    - `policy_analogs`
      - `id` (serial, primary key)
      - `policy_text` (text)
      - `historical_match` (text)
      - `similarity_score` (float)
      - `created_at` (timestamp)
  2. Security
    - Enable RLS on `policy_analogs` table
    - Add policy for authenticated users to read all data
*/

CREATE TABLE IF NOT EXISTS policy_analogs (
  id SERIAL PRIMARY KEY,
  policy_text TEXT NOT NULL,
  historical_match TEXT NOT NULL,
  similarity_score FLOAT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE policy_analogs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for authenticated users" 
  ON policy_analogs
  FOR SELECT
  TO authenticated
  USING (true);
