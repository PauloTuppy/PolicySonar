/*
  # Create simulations table

  1. New Tables
    - `simulations`
      - `id` (serial, primary key)
      - `policy_id` (integer, foreign key to policy_analogs)
      - `parameters` (jsonb)
      - `results` (jsonb)
      - `created_at` (timestamp)
  2. Security
    - Enable RLS on `simulations` table
    - Add policy for authenticated users to read their own data
*/

CREATE TABLE IF NOT EXISTS simulations (
  id SERIAL PRIMARY KEY,
  policy_id INTEGER REFERENCES policy_analogs(id),
  parameters JSONB,
  results JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE simulations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for own data" 
  ON simulations
  FOR SELECT
  TO authenticated
  USING (auth.uid() = (SELECT created_by FROM policy_analogs WHERE id = policy_id));
